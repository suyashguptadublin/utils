import pandas as pd
import sqlite3
import hashlib
import json

# Functions to compute checksums
def compute_schema_checksum(connection, table_name):
    """Compute SHA-256 checksum for table schema."""
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    schema_str = "|".join([f"{col[1]}:{col[2]}" for col in columns])  # col[1]=name, col[2]=type
    return hashlib.sha256(schema_str.encode('utf-8')).hexdigest()

def compute_data_checksum(connection, table_name):
    """Compute SHA-256 checksum for table data."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    data_str = "|".join([str(row) for row in rows])
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

# Function to process operations
def process_validation(connection, validation_df):
    cursor = connection.cursor()

    for _, row in validation_df.iterrows():
        function = row['Function']
        table_name = row['Table Name']
        column_def = row['Column Name']
        values = row['Values']
        expected_checksum = row['Expected Checksum']
        checksum_type = row['Checksum Type']

        try:
            if function == "Create Table":
                # Parse column definitions and constraints
                columns = column_def.split(",\n")
                create_columns = ", ".join(columns)
                sql = f"CREATE TABLE {table_name} ({create_columns})"
                cursor.execute(sql)
                print(f"Table {table_name} created successfully.")

            elif function == "Insert Table":
                # Parse and insert values
                columns = column_def.replace("\n", "").split(", ")
                data = json.loads(values.replace("'", '"'))
                for row_values in data:
                    placeholders = ", ".join(["?"] * len(row_values))
                    sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    cursor.execute(sql, row_values)
                print(f"Data inserted into {table_name} successfully.")

            elif function == "Check Table":
                # Validate checksum
                if checksum_type == "Structure":
                    current_checksum = compute_schema_checksum(connection, table_name)
                elif checksum_type == "Data":
                    current_checksum = compute_data_checksum(connection, table_name)
                else:
                    raise ValueError("Unknown checksum type.")

                if current_checksum == expected_checksum:
                    print(f"{checksum_type} checksum for {table_name} matches.")
                else:
                    print(f"{checksum_type} checksum for {table_name} does NOT match!")
                    print(f"Expected: {expected_checksum}, Got: {current_checksum}")

            elif function == "Post Operation Test":
                # Compute checksum post-operation
                if checksum_type == "Data":
                    current_checksum = compute_data_checksum(connection, table_name)
                    print(f"Post-operation checksum for {table_name} (Data): {current_checksum}")

            elif function == "DELETE":
                # Clear table contents
                sql = f"DELETE FROM {table_name}"
                cursor.execute(sql)
                print(f"Data deleted from {table_name}.")

            elif function == "DROP":
                # Drop the table
                sql = f"DROP TABLE {table_name}"
                cursor.execute(sql)
                print(f"Table {table_name} dropped.")

        except Exception as e:
            print(f"Error processing {function} for table {table_name}: {e}")

    connection.commit()

# Load Excel file
excel_file = "validation.xlsx"
validation_df = pd.read_excel(excel_file, sheet_name="Validation")

# Database setup (SQLite for example)
connection = sqlite3.connect(":memory:")

# Process validation operations
process_validation(connection, validation_df)

# Close connection
connection.close()
def generate_create_table_sql(row):
    """Generate SQL for creating a table based on the row."""
    table_name = row['Table Name']
    column_def = row['Column Name']
    constraint = row['Constraint']

    # Parse columns
    columns = column_def.split(",\n")  # Split by newlines
    columns = [col.strip().replace(":", " ") for col in columns]  # Convert "ID: INT" -> "ID INT"

    # Handle constraints
    if constraint and "PK" in constraint:
        constraint_col = constraint.split(":")[0].strip()
        for i, col in enumerate(columns):
            if col.startswith(constraint_col):
                columns[i] += " PRIMARY KEY NOT NULL"

    # Generate SQL
    sql = f"CREATE TABLE {table_name} (\n    {',\n    '.join(columns)}\n);"
    return sql, table_name
