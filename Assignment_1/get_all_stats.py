import csv
import sys

tsv_file = sys.argv[1]

with open(tsv_file, 'r', newline='', encoding='utf-8') as file:
    tsv_reader = csv.reader(file, delimiter='\t')

    # get column names
    header = next(tsv_reader)

    data_counts = {}
    empty_counts = {}

    # initialize dictionary
    for column in header:
        data_counts[column] = 0
        empty_counts[column] = 0
    
    filled_rows = 0
    empty_rows = 0

    for row in tsv_reader:
        empty = True
        full = True
        for i, cell in enumerate(row):
            column_name = header[i]
            if cell:
                # if one cell exists, it is not completely empty
                empty = False
                data_counts[column_name] += 1
            else:
                # if one cell doesn't exist, it is not completely full
                full = False
                empty_counts[column_name] += 1
        if empty:
            empty_rows += 1
        elif full:
            filled_rows += 1

for column in header:
    print(f"Column '{column}': Data Count = {data_counts[column]}, Empty Count = {empty_counts[column]}")

print(f"Completely Filled Rows: {filled_rows}")
print(f"Completely Empty Rows: {empty_rows}")
