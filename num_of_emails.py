import csv
import sys

# Replace 'your_file.tsv' with the actual path to your TSV file
tsv_file = sys.argv[1]
kwd_cnt = 0
non_cnt = 0
# Open the TSV file for reading
with open(tsv_file, 'r', newline='', encoding='utf-8') as file:
    # Create a CSV reader with tab delimiter
    tsv_reader = csv.reader(file, delimiter='\t')
    
    # Skip the header row if it exists
    next(tsv_reader, None)
    
    # Iterate through each row in the TSV file
    for row in tsv_reader:
        # Assuming Keywords is in the 6th column (index 5)
        emails = row[3]
        if emails and emails != 'no Emails':
            print(emails)
            kwd_cnt += 1
        else:
            non_cnt += 1

print(kwd_cnt)
print(non_cnt)
