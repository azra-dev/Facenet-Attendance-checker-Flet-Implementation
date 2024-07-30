import csv, os

def edit_data(file_path, column_header, row_value):
    rows = []
    column_index = None
    row_index = None

    if not os.path.exists(file_path):
        print(f"{file_path} does not exists")
        return None
    
    # Read
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            rows.append(row)
            if i == 0:  # Header row
                if column_header in row:
                    column_index = row.index(column_header)
            else:
                if row[0] == row_value:
                    row_index = i

    # Check if exists
    if column_index is None:
        column_index = len(rows[0])
        rows[0].append(column_header)  # Add new column header
        for row in rows[1:]:
            row.append('0')  # Initialize the new column with '0'
        print(f"Column header '{column_header}' not found. Created new column.")

    # If sit-in exists
    if row_index is None:
        print(f"Row with first column value '{row_value}' not found.")
        return

    # Write
    rows[row_index][column_index] = "1"
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)
    
    print(f"Modified cell at row {row_index}, column {column_index}.")
