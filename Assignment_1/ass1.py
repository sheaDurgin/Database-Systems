import os
from bs4 import BeautifulSoup

# Shea and SJ

# Path to the folder containing HTML files
folder_path = '../arxiv-papers/'

# Get a sorted list of HTML files in the folder
html_files = sorted([filename for filename in os.listdir(folder_path) if filename.endswith('.html')])

# Loop through all sorted HTML files in the folder
for filename in html_files:
    if filename.endswith('.html'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as html_file:
            content = html_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            title = soup.title.text
            print(f"Title: {title}")

            authors = soup.find_all('div', class_='ltx_authors')
            author_info = []

            for author in authors:
                name = author.find('span', class_='ltx_personname').get_text(strip=True)
                
                # Check if affiliation element exists
                affiliation_element = author.find('span', class_='ltx_role_address')
                affiliation = affiliation_element.get_text(strip=True) if affiliation_element else ""
                
                email_element = author.find('span', class_='ltx_role_email')
                email = email_element.get_text(strip=True) if email_element else ""
                
                author_info.append({'name': name, 'affiliation': affiliation, 'email': email})

            abstract = soup.find('p', class_='ltx_p').get_text(strip=True)

            keywords_element = soup.find('div', class_='ltx_classification')
            keywords = []
            if keywords_element:
                keywords_text = keywords_element.get_text(strip=True)
                if "keywords:" in keywords_text.lower():
                    keywords_text = keywords_text.lower().replace("keywords:", "")
                    keywords = [keyword.strip() for keyword in keywords_text.split(',')]
                elif filename in keywords_text.lower():
                    keywords_text = keywords_text.lower().replace("keywords:", "")
                    keywords = [keyword.strip() for keyword in keywords_text.split(',')]

            print("Author Info:", author_info)
            print("Abstract:", abstract)
            print("Keywords:", keywords)
            print("=" * 50)  # Just for separating output between files
