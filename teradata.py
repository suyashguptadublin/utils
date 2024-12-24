try:
    conn = teradatasql.connect(host="ncrdwprod.aib.pri", user="DW79940", password=password, logmech="LDAP")
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE")
    print("Current Database", cursor.fetchone()[0])

    #List all databases

    cursor.execute("""SELECT TableName, TableKind from DBC.Tables WHERE DatabaseName = 'ddewd06s';""")
    print("Databases")
    for row in cursor.fetchall():
        print(row[0], row[1])
    # con.close()


except Exception as ex:
    print("error", ex)
    print(traceback.format_exc())
finally:
    conn.close()
#### context manager

from contextlib import contextmanager
import teradatasql
import traceback

@contextmanager
def teradata_connection(config):
    """
    Context manager for Teradata database connection and cursor.
    Automatically opens and closes the connection and cursor.
    """
    connection = None
    cursor = None
    try:
        # Establish the connection
        connection = teradatasql.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            logmech=config["logmech"]
        )
        cursor = connection.cursor()
        print("Database connection established.")
        yield cursor  # Provide the cursor for executing queries
    except Exception as ex:
        print("Error during database operation:", ex)
        print(traceback.format_exc())
    finally:
        if cursor:
            cursor.close()
            print("Cursor closed.")
        if connection:
            connection.close()
            print("Connection closed.")

# Example Usage
def main():
    # Configuration for the connection
    config = {
        "host": "ncrdwprod.aib.pri",
        "user": "DW79940",
        "password": "your_password_here",  # Replace with your actual password
        "logmech": "LDAP"
    }

    with teradata_connection(config) as cursor:
        # Get the current database
        cursor.execute("SELECT DATABASE")
        print("Current Database:", cursor.fetchone()[0])

        # List all tables in a specific database
        cursor.execute("SELECT TableName, TableKind FROM DBC.Tables WHERE DatabaseName = 'ddewd06s';")
        print("Tables in 'ddewd06s':")
        for row in cursor.fetchall():
            print(row[0], row[1])

        # Add more operations as needed here
        # Example: Create a table
        create_query = """
        CREATE TABLE ddewd06s.sample_table (
            id INTEGER,
            name VARCHAR(100)
        );
        """
        try:
            cursor.execute(create_query)
            print("Table 'sample_table' created successfully.")
        except Exception as ex:
            print("Error during table creation:", ex)

if __name__ == "__main__":
    main()
