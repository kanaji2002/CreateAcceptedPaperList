# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

import os
import pandas as pd

# URL of the page containing accepted papers
year = 2026

separater = "<SEP>"
file_path = os.path.join("url", f"{year}.csv")
# CSVファイルを読み取り、DataFrameとして格納
df = pd.read_csv(file_path, header=None)
df.columns = ['name', 'track', 'url'] # ヘッダーを指定

error_list = []

output_path = os.path.join("out", f"{year}_out.csv")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("Conference,Type,Title,In Charge,Presentation year\n")
    for _, row in df.iterrows():
        name = row['name']
        track = row['track']
        url = row['url']

        if not isinstance(url, str):
            error_list.append(f"{name}{separater}{track}{separater}No URL is given")
            continue
        # Send a GET request to the URL
        try:
            response = requests.get(url)
        except:
            error_list.append(f"{name}{separater}{track}{separater}HTTP Errors")
            continue
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            tag = soup.find('div', id='event-overview')
            if tag is None:
                error_list.append(f"{name}{separater}{track}{separater}Accepted table is not ready")
                continue

            table = tag.find('table', class_='table table-condensed')

            # Find all paper titles on the page
            paper_links = table.find_all('a', {'data-event-modal': True})

            # Extract and print the paper titles
            papers = [link.contents[0].strip() for link in paper_links]

            # print("Accepted Papers:")
            for paper in papers:
                f.write(f"{name},{track},{paper},,\n")
        else:
            error_list.append(f"{name}{separater}{track}{separater}Anonymous Errors")

    for e in error_list:
        f.write(f"{e}\n")
