"""
Uses BeautifulSoup to scrape the New York Times bestseller website.
Prints information on the bestsellers and writes it out to a CSV file.
Uses pandas to read information in the CSV file and prints a summary of
the bestsellers that are new this week.
"""
import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.nytimes.com/books/best-sellers/hardcover-fiction/"
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

names = soup.find_all("h3", itemprop="name")
nums = soup.find_all("p", class_="css-1o26r9v")
authors = soup.find_all("p", itemprop="author")
publishers = soup.find_all("p", itemprop="publisher")
descriptions = soup.find_all("p", itemprop="description")

names = [name.text.title() for name in names]
num_weeks = [num.text for num in nums]
authors = [author.text.lstrip("by ") for author in authors]
publishers = [publisher.text for publisher in publishers]
descriptions = [description.text for description in descriptions]

num_weeks = [item.replace(" weeks on the list", "") for item in num_weeks]
num_weeks = [item.replace("New this week", "0") for item in num_weeks]
num_weeks = [int(num) for num in num_weeks]

books = list(zip(names, num_weeks, authors, publishers, descriptions))

books.sort(key=lambda book: book[1])
print("=========================================")
for book in books:
    print(f"Title: {book[0]}")
    print(f'Number of weeks on the list: {"Newly added " if book[1] == 0 else book[1]}')
    print(f"Author: {book[2]}")
    print(f"Publisher: {book[3]}")
    print(f"Description: {book[4]}")
    print("=========================================")

header = ["Title", "# weeks on list", "Author", "Publisher", "Description"]

with open("best_sellers.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(header)
    writer.writerows(books)

df = pd.read_csv("best_sellers.csv", delimiter=",")
print()
print("NEW THIS WEEK: ")
print("-------------")
print(df[df["# weeks on list"] == 0]["Title"])
