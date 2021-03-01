import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

munro_domains = [
    url.strip() for url in open("munro_urls.txt").read().split("\n") if url
]


for domain in munro_domains:
    page_content = requests.get(domain).text

    soup = BeautifulSoup(page_content, features="html.parser")

    # Munro Name
    name = soup.find("h1").find("span").text.strip()
    print(name)

    # Munro Height
    altitude_string = soup.select_one('p:-soup-contains("Altitude")').text.strip()
    altitude_string = altitude_string[len("Altitude: ") :].strip()
    altitude_string = altitude_string.removesuffix(" metres")
    print(altitude_string)

    # Munro Region
    region_string = soup.select_one('p:-soup-contains("Region")').find("a").text
    print(region_string)

    # Munro Rating
    rating = soup.find("strong").text.strip()
    print(rating)

    # Munro Route
    routes_heading = soup.select_one('h2:-soup-contains("Detailed route")')
    routes = routes_heading.find_next_sibling().find_all('a')
    for link in routes:
        print(link.get("href"))