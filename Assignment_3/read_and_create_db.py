import json
from tqdm import tqdm
import re
import sqlite3

# ~/Desktop/DatabaseSystems/Assignment3/arxiv_db.db

with open('arXiv21.json', 'r', encoding="utf-8") as json_file:
    total_lines = sum(1 for _ in json_file)

data_rows = []

def get_name(name):
    return (' '.join(name.split()[1:]), name.split()[0])

# unique_categories = set()

# if you are writing csv file make sure to set encoding
with open('arXiv21.json', 'r', encoding="utf-8") as json_file:
    for line in tqdm(json_file, total=total_lines):
        # data is a dictionary of attributes
        paper = json.loads(line)
        paper_id = paper['id']
        lst_author = [get_name(name) for name in paper['authors']]
        unique_lst_author = list(set(lst_author))
        submitter = get_name(paper['submitter'])
        title = paper['title']
        categories = paper['categories']
        category_list = categories.split(" ")
        last_update = paper['last_update']
        lst_cited = re.findall(r"'([^']*)'", paper['cited'])
        
        unique_lst_cited = list(set(lst_cited))

        # for category in category_list:
        #     unique_categories.add(category)

        # Create a list to represent a row of data
        row = [paper_id, unique_lst_author, submitter, title, category_list, last_update, unique_lst_cited]

        # Append the row to the data_rows list
        data_rows.append(row)

db_file_name = 'arxiv_db.db'  # Change the name here

# Connect to the SQLite database
conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

# Create the Author table
cursor.execute('''CREATE TABLE Author (
    FNAME TEXT,
    LNAME TEXT,
    PRIMARY KEY (FNAME, LNAME)
)''')

# Create the Paper table
cursor.execute('''CREATE TABLE Paper (
    ID TEXT PRIMARY KEY,
    LastUpdate TEXT,
    Title TEXT,
    SubmitterFNAME TEXT,
    SubmitterLNAME TEXT,
    FOREIGN KEY (SubmitterFNAME, SubmitterLNAME) REFERENCES Author (FNAME, LNAME)
)''')

# Create the Write relationship table
cursor.execute('''CREATE TABLE Write (
    FNAME TEXT,
    LNAME TEXT,
    PaperID TEXT,
    PRIMARY KEY (FNAME, LNAME, PaperID),
    FOREIGN KEY (FNAME, LNAME) REFERENCES Author (FNAME, LNAME),
    FOREIGN KEY (PaperID) REFERENCES Paper (ID)
)''')

# Create the Cites relationship table
cursor.execute('''CREATE TABLE Cites (
        CitingPaperID TEXT,
        CitedPaperID TEXT,
        PRIMARY KEY (CitingPaperID, CitedPaperID),
        FOREIGN KEY (CitingPaperID) REFERENCES Paper (ID),
        FOREIGN KEY (CitedPaperID) REFERENCES Paper (ID)
)''')

# # Create the Category table
# cursor.execute('''CREATE TABLE Category (
#         Category TEXT PRIMARY KEY
# )''')

# Create the Paper_To_Category relationship table
cursor.execute('''CREATE TABLE Paper_To_Category (
        PaperID TEXT,
        Category TEXT,
        PRIMARY KEY (PaperID, Category),
        FOREIGN KEY (PaperID) REFERENCES Paper (ID)
)''')

# for category in unique_categories:
#     cursor.execute("INSERT INTO Category (Category) VALUES (?)", (category, ))

for row in tqdm(data_rows):
    paper_id, author_tuples, submitter, title, category_list, last_update, lst_cited = row

    # Insert data into the Author and Paper tables
    for author_tuple in author_tuples:
        cursor.execute("INSERT OR IGNORE INTO Author (FNAME, LNAME) VALUES (?, ?)", (author_tuple))

    cursor.execute("INSERT INTO Paper (ID, LastUpdate, Title, SubmitterFNAME, SubmitterLNAME) VALUES (?, ?, ?, ?, ?)",
                    (paper_id, last_update, title, submitter[0], submitter[1]))

    # Insert data into the Write relationship table
    for author_tuple in author_tuples:
        cursor.execute("INSERT INTO Write (FNAME, LNAME, PaperID) VALUES (?, ?, ?)", (*author_tuple, paper_id))

    for cite in lst_cited:
        cursor.execute("INSERT INTO Cites (CitingPaperID, CitedPaperID) VALUES (?, ?)", (paper_id, cite))

    for category in category_list:  
        cursor.execute("INSERT INTO Paper_To_Category (PaperID, Category) VALUES (?, ?)", (paper_id, category))

# Commit the changes and close the database connection
conn.commit()
conn.close()
