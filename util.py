import openpyxl
import json

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

def read_group_names_xls(file_path):
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


def read_group_names_txt(file_path):
    groupnames = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('/')
                if len(parts) >= 3:
                    username = parts[3]
                    groupnames.append(username)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return groupnames

