# Database Systems Assignment 1

This folder contains the program to scrape ar5ive html files into a tsv and a program to retrieve the stats of the outputted tsv. The data it scrapes includes, Title, Author Names, Affiliations, Emails, Abstract, and Keywords. This program was developed by both Shea Durgin and SJ Franklin equally.

## Table of Contents

- [Installation](#Installation)
- [Steps to Run](#Steps-to-Run)
- [Program Details](#Program-Details)
- [Results](#Results)
- [Conclusion](#Conclusion)

## Installation

To run this code, you will need to download arxiv papers as html from [ar5ive](https://ar5iv.labs.arxiv.org).

You can either clone the entire repository or this folder specifically, you can do so by following these steps:

    Move to the directory you want to clone to
    git init <repository>
    cd <repository>
    git remote add -f origin <repository>
    git config core.sparseCheckout true
    echo "Assignment_1/" >> .git/info/sparse-checkout
    git pull origin main

The necessary installs for the code are as such:

    beautifulsoup4
    tqdm

You can install them using pip:

    pip install beautifulsoup4 tqdm

## Steps to Run

- Update directory to folder with ar5ive html files
- Optional: Update outputted tsv name, however this is not required
- Run scrape_ar5ive_files.py
- Optional: Run get_all_stats.py with the tsv file as an argument

## Program Details
Our program uses a combination of both regex techniques and the beautifulsoup library to scrape useful information from ar5ive html files.

## Results
    Column 'Title': Data Count = 2748, Empty Count = 0
    Column 'Author Names': Data Count = 2191, Empty Count = 557
    Column 'Affiliations': Data Count = 1667, Empty Count = 1081
    Column 'Emails': Data Count = 1645, Empty Count = 1103
    Column 'Abstract': Data Count = 2352, Empty Count = 396
    Column 'Keywords': Data Count = 988, Empty Count = 1760
    Completely Filled Rows: 656
    Completely Empty Rows: 0

## Conclusion
The data extraction process captures a subset of the content available in arXiv papers. There is room for further refinement to extract affiliations, email addresses, and keywords more effectively. Exploring alternative methods for keyword extraction, such as employing YAKE!, is also worth considering.

However, it's important to acknowledge that some data may remain elusive in these papers. This is due to the absence of a consistent pattern across all papers. Enforcing a uniform extraction method for all papers is likely to miss out on unique cases and may not fully resolve missing data issues.