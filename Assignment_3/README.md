# Database Systems Assignment 3

This folder contains the program to read arXiv paper data in a json format to construct a sqlite datbase to perform many sql queries on.

## Table of Contents

- [Installation](#Installation)
- [Steps to Run](#Steps-to-Run)

## Installation

You can either clone the entire repository or this folder specifically, you can do so by following these steps:

    Move to the directory you want to clone to
    git init <repository>
    cd <repository>
    git remote add -f origin <repository>
    git config core.sparseCheckout true
    echo "Assignment_3/" >> .git/info/sparse-checkout
    git pull origin main

The necessary installs for the code are as such:

    tqdm

You can install them using pip:

    pip install tqdm

## Steps to Run

- Run read_and_create_db.py