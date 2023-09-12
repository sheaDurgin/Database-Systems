import os
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import re

def clean_text(text):
    # Remove newline and tab characters, and replace them with spaces
    return ' '.join(text.strip().split())

def extract_text_from_spans(element, class_name, element_name):
    spans = element.find_all('span', class_=class_name)
    if spans:
        return ' '.join([clean_text(span.get_text(strip=True)) for span in spans])
    else:
        return f"no {element_name}"

def extract_keywords(keywords_element):
    keywords = []
    if keywords_element:
        keywords_text = clean_text(keywords_element.get_text(strip=True))
        pattern = re.compile(r'\b(key ?-?words)(.*)\s*:\s*')
        if re.search(pattern, keywords_text.lower()):
            keywords_text = re.sub(pattern, "", keywords_text.lower())
        if "keywords:" in keywords_text.lower():
            keywords_text = keywords_text.lower().replace("keywords:", "")
        if "index terms:" in keywords_text.lower():
            keywords_text = keywords_text.lower().replace("keywords:", "")
        keywords = [keyword.strip() for keyword in keywords_text.split(',')]
    return keywords

def remove_superscripts(soup):
    # may need to add more elements
    for element in soup.find_all('math'):
        element.extract()

# folder_path = '../arxiv-papers/'
#folder_path = '../../../../shea.durgin/Database-Systems/arxiv-papers/'
folder_path = '../arxiv-papers/'
# chane to within Ass1 folder
output_tsv_path = '../output_testing5.tsv'

html_files = sorted([filename for filename in os.listdir(folder_path) if filename.endswith('.html')])

def scrape_emails_from_html(soup):
    # Define a regular expression pattern to match email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # Find all email addresses in the HTML using the re.findall method
    emails = re.findall(email_pattern, str(soup))

    unique_emails = list(set(emails))

    return unique_emails

def process_html_file(filename):
    if filename.endswith('.html'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as html_file:
            content = html_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            title = clean_text(soup.title.text)

            authors = soup.find_all('div', class_='ltx_authors')
            remove_superscripts(soup)
            author_names = [extract_text_from_spans(author, 'ltx_personname', 'Author Names') for author in authors]
            affiliations = [extract_text_from_spans(author, 'ltx_role_address', 'Affiliations') for author in authors]
            #emails = [extract_text_from_spans(author, 'ltx_role_email', 'Emails') for author in authors]
            emails = scrape_emails_from_html(soup)

            abstract_element = soup.find('p', class_='ltx_p')
            abstract = clean_text(abstract_element.get_text(strip=True)) if abstract_element else ""

            pattern = re.compile(r'.*key ?-?words.*', re.IGNORECASE)
            keywords_element = soup.find('div', class_="ltx_keywords") or soup.find('div', class_='ltx_classification') or soup.find(['div', 'span'], string=pattern)
            # keywords_element = soup.find(['div', 'span'], text=pattern)
            keywords = extract_keywords(keywords_element)

            return [title, ' '.join(author_names), ' '.join(affiliations), ' '.join(emails), abstract, ' | '.join(keywords)]

# Process HTML files in parallel (and use progress bar)
with ProcessPoolExecutor() as executor:
    results = list(tqdm(executor.map(process_html_file, html_files), total=len(html_files), desc="Reading HTML Files"))

# Write to TSV file
with open(output_tsv_path, 'w', encoding='utf-8', newline='') as output_tsv:
    tsv_writer = csv.writer(output_tsv, delimiter='\t')
    # Header row
    tsv_writer.writerow(["Title", "Author Names", "Affiliations", "Emails", "Abstract", "Keywords"])

    for result in results:
        tsv_writer.writerow(result)
