import json
from tqdm import tqdm
import csv
import re

with open('arXiv21.json', 'r', encoding="utf-8") as json_file:
    total_lines = sum(1 for _ in json_file)

data_rows = []

# if you are writing csv file make sure to set encoding
with open('arXiv21.json', 'r', encoding="utf-8") as json_file:
    for line in tqdm(json_file, total=total_lines):
        # data is a dictionary of attributes
        paper = json.loads(line)
        paper_id = paper['id']
        lst_author = [(name.split()[-1], name.split()[0]) for name in paper['authors']]
        submitter = paper['submitter'].split()[-1] + ' ' + paper['submitter'].split()[0]
        title = paper['title']
        categories = paper['categories']
        last_update = paper['last_update']
        lst_cited = re.findall(r"'([^']*)'", paper['cited'])

        # Create a list to represent a row of data
        row = [paper_id, lst_author, submitter, title, categories, last_update, lst_cited]

        # Append the row to the data_rows list
        data_rows.append(row)

# # Define the CSV file name
# csv_file_name = 'arXiv21.csv'

# # Write the data to the CSV file
# with open(csv_file_name, 'w', encoding='utf-8', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)

#     # Write the header row (column names)
#     csv_writer.writerow(['id', 'authors', 'submitter', 'title', 'categories', 'last_update', 'cited'])

#     # Write the data rows
#     for row in data_rows:
#         csv_writer.writerow(row)

        
