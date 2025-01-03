import sys
import pandas as pd
import hashlib

class ExcelOperationFramework:
    def __init__(self, excel_sheet_name, tab_name, function_name):
        """
        Initialize the framework with an Excel file, tab name, and function name.

        Args:
            excel_sheet_name (str): Path to the Excel file.
            tab_name (str): Name of the tab (sheet) in the Excel file.
            function_name (str): The name of the function to execute.
        """
        self.excel_sheet_name = excel_sheet_name
        self.tab_name = tab_name
        self.function_name = function_name

    def execute(self):
        """
        Execute the specified function on the Excel tab.

        Returns:
            The result of the function applied to the data.
        """
        try:
            # Load the Excel sheet
            data = pd.read_excel(self.excel_sheet_name, sheet_name=self.tab_name)

            # Dynamically resolve the function name
            function = globals().get(self.function_name)
            if not function:
                raise ValueError(f"Function '{self.function_name}' not found.")

            # Execute the function on the data
            result = function(data)

            # Return the result
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

def compute_sha256_from_list(input_list):
    """
    Compute a consistent SHA-256 hash from a list of tuples.
    
    Args:
        input_list (list of tuple): A list of tuples where each tuple consists of
                                    an index (key) and a value.
                                    Example: [(TestCol001, 46), (TestCol002, 20)]
    
    Returns:
        str: A SHA-256 hash string.
    """
    # Step 1: Sort the list of tuples by the key (first item in each tuple)
    sorted_list = sorted(input_list, key=lambda x: x[0])
    
    # Step 2: Convert the sorted list into a string representation
    # Ensure consistent string format for hashing
    concatenated_string = "|".join(f"{key}:{value}" for key, value in sorted_list)
    
    # Step 3: Compute the SHA-256 hash
    sha256_hash = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()
    
    return sha256_hash



def create_table_sql(tab_data, sha_ref_tab=None):
    """
    Generate a CREATE TABLE statement based on the properties in the CreateTable tab.

    Args:
        tab_data (DataFrame): The data from the CreateTable tab.
        sha_ref_tab (DataFrame): Not required for table creation but included for consistency.

    Returns:
        str: The generated CREATE TABLE SQL statement.
    """
    # Ensure the tab has the required structure
    if 'ObjectType' not in tab_data.columns or 'ObjectName' not in tab_data.columns:
        raise ValueError("The tab is missing required columns 'ObjectType' and 'ObjectName'.")

    # Extract database and table names
    database = tab_data.loc[tab_data['ObjectType'] == 'Database', 'ObjectName'].values[0]
    table = tab_data.loc[tab_data['ObjectType'] == 'Table', 'ObjectName'].values[0]

    # Extract column definitions
    columns = tab_data[tab_data['ObjectType'] == 'Column']
    if columns.empty:
        raise ValueError("No columns defined in the tab.")

    column_definitions = []
    for _, row in columns.iterrows():
        column_name = row['ObjectName']
        column_type = row['ObjectAttribute']
        column_definitions.append(f"{column_name} {column_type}")

    # Construct the CREATE TABLE SQL statement
    column_definitions_str = ",\n    ".join(column_definitions)
    create_table_sql = f"CREATE TABLE {database}.{table} (\n    {column_definitions_str}\n);"

    print(create_table_sql)

    return create_table_sql

# Example operation functions
def compute_sha256(data):
    """Compute SHA-256 hash for each row."""
    def hash_row(row):
        row_data = "|".join(str(value) for value in row)
        return hashlib.sha256(row_data.encode('utf-8')).hexdigest()

    data['SHA-256'] = data.apply(hash_row, axis=1)
    return data

def count_rows(data):
    """Count the number of rows in the sheet."""
    return len(data)


if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python excel_operations.py <excel_file> <sheet_name> <function_name>")
        sys.exit(1)

    excel_file = sys.argv[1]
    sheet_name = sys.argv[2]
    function_name = sys.argv[3]

    # Run the framework
    framework = ExcelOperationFramework(excel_file, sheet_name, function_name)
    result = framework.execute()

    if result is not None:
        if isinstance(result, pd.DataFrame):
            print("Operation Result:")
            print(result)
        else:
            print(f"Operation Result: {result}")
