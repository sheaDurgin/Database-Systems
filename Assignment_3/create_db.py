import sqlite3
import csv
import re

# ~/Desktop/DatabaseSystems/Assignment3/arxiv_database.db

def extract_tuples(input_string):
    # Define a regex pattern to match tuples inside square brackets
    pattern = r'\(\s*\'([\w\s]+)\'\s*,\s*\'([\w\s]+)\'\s*\)'

    # Use re.findall to find all matches in the input string
    matches = re.findall(pattern, input_string)

    # Convert the matches to a list of tuples
    result = [(match[0], match[1]) for match in matches]

    return result

# Specify your CSV file and the desired SQLite database file name
csv_file_name = 'arXiv21.csv'
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
    Category TEXT,
    LastUpdate TEXT,
    Title TEXT
)''')

# Create the Write relationship table
cursor.execute('''CREATE TABLE Write (
    FNAME TEXT,
    LNAME TEXT,
    PaperID TEXT,
    FOREIGN KEY (FNAME, LNAME) REFERENCES Author (FNAME, LNAME),
    FOREIGN KEY (PaperID) REFERENCES Paper (ID)
)''')

# Create the Submit relationship table
cursor.execute('''CREATE TABLE Submit (
    FNAME TEXT,
    LNAME TEXT,
    PaperID TEXT,
    FOREIGN KEY (FNAME, LNAME) REFERENCES Author (FNAME, LNAME),
    FOREIGN KEY (PaperID) REFERENCES Paper (ID)
)''')

# Create the Cites relationship table
cursor.execute('''CREATE TABLE Cites (
    CitingPaperID TEXT,
    CitedPaperID TEXT,
    FOREIGN KEY (CitingPaperID) REFERENCES Paper (ID),
    FOREIGN KEY (CitedPaperID) REFERENCES Paper (ID)
)''')

# Read the data from the CSV file and insert it into the Author and Paper tables
with open(csv_file_name, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        paper_id, lst_author, submitter, title, categories, last_update, lst_cited = row
        author_tuples = extract_tuples(lst_author)
        # Insert data into the Author and Paper tables
        for author_tuple in author_tuples:
            cursor.execute("INSERT OR IGNORE INTO Author (FNAME, LNAME) VALUES (?, ?)", (author_tuple))

        cursor.execute("INSERT INTO Paper (ID, Category, LastUpdate, Title) VALUES (?, ?, ?, ?)",
                       (paper_id, categories, last_update, title))

        # Insert data into the Write and Submit relationship tables
        for author_tuple in author_tuples:
            cursor.execute("INSERT INTO Write (FNAME, LNAME, PaperID) VALUES (?, ?, ?)", (*author_tuple, paper_id))

        cursor.execute("INSERT INTO Submit (FNAME, LNAME, PaperID) VALUES (?, ?, ?)", (submitter.split()[0], submitter.split()[1], paper_id))

# Commit the changes and close the database connection
conn.commit()
conn.close()
