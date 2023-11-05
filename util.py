import openpyxl

def read_group_names(file_path):
    sheetname = "Telegram"
    column_name = "Source ID"
    values = []

    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheetname]

        # Find the column index based on the column name
        column_index = None
        for cell in sheet[1]:
            if cell.value == column_name:
                column_index = cell.column
                break

        if column_index is not None:
            # Iterate through the rows and append values from the specified column to the list
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[column_index - 1] != None:
                    values.append(row[column_index - 1])
                    
                    

    except Exception as e:
        print(f"Error reading the XLSX file: {e}")

    values = [url.split('/')[-1] for url in values]
    return values

# Example usage
file_path = "MASTER_NAWA_GAZA_Sources_2023_data_collecting.xlsx"
values_list = read_group_names(file_path)
print(values_list)