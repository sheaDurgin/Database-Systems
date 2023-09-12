import csv
import sys

# Replace 'your_file.tsv' with the actual path to your TSV file
tsv_file = sys.argv[1]

# Open the TSV file for reading
with open(tsv_file, 'r', newline='', encoding='utf-8') as file:
    # Create a CSV reader with tab delimiter
    tsv_reader = csv.reader(file, delimiter='\t')

    # Read the header row to get column names
    header = next(tsv_reader)

    # Initialize dictionaries to store counts for each column
    data_counts = {}
    empty_counts = {}

    # Initialize counters for data and empty cells
    for column in header:
        data_counts[column] = 0
        empty_counts[column] = 0
    
    # Initialize counters for completely filled and completely empty rows
    filled_rows = 0
    empty_rows = 0

    # Iterate through each row in the TSV file
    for row in tsv_reader:
        empty = True
        full = True
        # Iterate through each column in the row
        for i, cell in enumerate(row):
            column_name = header[i]
            if cell:
                empty = False
                data_counts[column_name] += 1
            else:
                full = False
                empty_counts[column_name] += 1
        if empty:
            empty_rows += 1
        elif full:
            filled_rows += 1
# Print the counts for each column
for column in header:
    print(f"Column '{column}': Data Count = {data_counts[column]}, Empty Count = {empty_counts[column]}")

# Print the counts for completely filled rows and completely empty rows
print(f"Completely Filled Rows: {filled_rows}")
print(f"Completely Empty Rows: {empty_rows}")
