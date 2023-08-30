import os
from bs4 import BeautifulSoup

def clean_text(text):
    # Remove newline and tab characters, and replace them with spaces
    return ' '.join(text.strip().split())

def extract_author_info(author):
    name = clean_text(author.find('span', class_='ltx_personname').get_text(strip=True))
    affiliation_element = author.find('span', class_='ltx_role_address')
    affiliation = clean_text(affiliation_element.get_text(strip=True)) if affiliation_element else ""
    email_element = author.find('span', class_='ltx_role_email')
    email = clean_text(email_element.get_text(strip=True)) if email_element else ""
    return {'name': name, 'affiliation': affiliation, 'email': email}

def extract_keywords(keywords_element):
    keywords = []
    if keywords_element:
        keywords_text = clean_text(keywords_element.get_text(strip=True))
        if "keywords:" in keywords_text.lower():
            keywords_text = keywords_text.lower().replace("keywords:", "")
            keywords = [keyword.strip() for keyword in keywords_text.split(',')]
    return keywords

folder_path = '../arxiv-papers/'
output_tsv_path = '../output.tsv'

html_files = sorted([filename for filename in os.listdir(folder_path) if filename.endswith('.html')])

with open(output_tsv_path, 'w', encoding='utf-8') as output_tsv:
    output_tsv.write("Title\tAuthor Names\tAuthor Affiliations\tAuthor Emails\tAbstract\tKeywords\n")

    for filename in html_files:
        if filename.endswith('.html'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as html_file:
                content = html_file.read()
                soup = BeautifulSoup(content, 'html.parser')

                title = clean_text(soup.title.text)
                authors = soup.find_all('div', class_='ltx_authors')
                author_info_list = [extract_author_info(author) for author in authors]
                abstract = clean_text(soup.find('p', class_='ltx_p').get_text(strip=True))
                keywords_element = soup.find('div', class_='ltx_classification')
                keywords = extract_keywords(keywords_element)

                for author_info in author_info_list:
                    output_line = f"{title}\t{author_info['name']}\t{author_info['affiliation']}\t{author_info['email']}\t{abstract}\t{' | '.join(keywords)}\n"
                    output_tsv.write(output_line)
