

def compute_signature_with_order(values, selection_order):
    """
    Compute a hash signature for values based on a specific selection order.
    Args:
        values (str): String of values in a structured format (e.g., JSON-like or list of lists).
                      Example: "[[1, 'RED', '353XXXX'], [2, 'GREEN', '353XXXY']]"
        selection_order (str): Comma-separated string specifying the selection order.
                               Example: "ID,NAME,PHONE"
    Returns:
        str: SHA-256 hash representing the reordered values' signature.
    """
    try:
        # Parse the values and selection order
        parsed_values = eval(values)  # Converts string representation to Python list
        selection_order = [col.strip() for col in selection_order.split(",")]

        # Ensure values match the selection order
        if len(parsed_values[0]) != len(selection_order):
            raise ValueError("Number of columns in 'Values' does not match the 'Selection Order'.")

        # Normalize data based on selection order
        normalized_data = []
        for row in parsed_values:
            # Reorder row values based on the selection order
            reordered_row = [str(row[selection_order.index(col)]) for col in selection_order]
            normalized_data.append("|".join(reordered_row))  # Join reordered values with "|"

        # Join all rows into a single string
        data_string = "\n".join(normalized_data)

        # Compute and return the hash
        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    except Exception as e:
        print(f"Error computing signature: {values}, {selection_order}. Exception: {e}")
        raise ValueError("Error computing checksum")


def calculate_and_save_checksums_data(file_path, sheet_name):
    """
    Compute and save hash signatures based on values in an Excel sheet.
    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to update.
    """
    # Load the workbook and sheet
    workbook = load_workbook(file_path)
    sheet = workbook[sheet_name]

    # Identify column indexes
    headers = [cell.value for cell in sheet[1]]  # First row as headers
    function_col = headers.index("Function") + 1
    order = headers.index("Selection Order") + 1
    values_col = headers.index("Values") + 1
    computed_signature_col = headers.index("Computed Checksum") + 1

    # Iterate through rows
    for row in range(2, sheet.max_row + 1):  # Skip header row
        function = sheet.cell(row=row, column=function_col).value

        # Process rows with function 'Check Table Records'
        if function == "Check Table Records":
            values = sheet.cell(row=row, column=values_col).value
            selection_order = sheet.cell(row=row, column = order).value

            if values:
                print(selection_order)
                # Parse values and compute the hash
                computed_signature = compute_signature_with_order(values, selection_order)

                # Save the computed signature
                sheet.cell(row=row, column=computed_signature_col, value=computed_signature)
            else:
                print(f"Row {row}: 'Values' is empty, skipping.")
        # Save the updated workbook
    workbook.save(file_path)
    print(f"Updated Excel file saved at {file_path}")





config_path = "config.yaml"
config = load_config(config_path)
excel_path = config["excel"]["file_path"]
sheet_name = config["excel"]["sheet_name"]

calculate_and_save_checksums_data(excel_path, sheet_name)





for _, row in validation_df.iterrows():
        #print('test', _, row)
        function = row['Function']
        table_name = row['Table Name']
        column_def = row['Column Name']
        values = row['Values']
        selection_order = row["Selection Order"]
     

        #print(function, table_name, column_def, values, expected_checksum, checksum_type)

      
        if function == "Create Table":
            get_sql_query, table_name = generate_create_table_sql(row)
        #     #print(get_sql_query)
        #     execute_sql_query(get_sql_query)
        #     print(f"Table {table_name} created successfully.")
            
        # elif function == "Check Table Schema":
        #     # Check Table logic
        #     computed_checksum = compute_table_structure_hash(column_def)
        #     pre_computed_schema = row['Computed Checksum']
        #     if computed_checksum == pre_computed_schema:
        #         print(f"Cheksum for {table_name} is verified successfully")
        #     else:
        #         raise ValueError("Checksum Mismatched")

        # elif function == "Insert Table":
        #     get_insert_sqls, table_name = generate_insert_sql(row)
        #     #print(get_insert_sqls, table_name)
        #     execute_sql_query(get_insert_sqls, operation_type="insert")

        elif function == "Check Table Records":
            print(selection_order)
            computed_checksum = compute_signature_with_order(column_def, selection_order)
            pre_computed_schema = row['Computed Checksum']
            print(computed_checksum, pre_computed_schema)
            if computed_checksum == pre_computed_schema:
                pass
            else:
                raise ValueError("Checksum Mismatched")
