import requests
from pprint import pprint
import re
from bs4 import BeautifulSoup

url = "https://www.walkhighlands.co.uk/munros/munros-a-z"
page = requests.get(url)

page_content = page.text
soup = BeautifulSoup(page_content, features="html.parser")

tables = soup.find_all("tbody")
munros = []
munro_links = []

f = open("munro_urls.txt", "a")

for table in tables:
    for link in table.find_all("a"):
        munro = link.get("href")
        print(munro)
        munros.append(munro)
        munro_link = f"https://www.walkhighlands.co.uk/munros/{munro}\n"
        f.write(munro_link)

f.close()
print(len(munros))