import json
import requests
from bs4 import BeautifulSoup


munro_domains = [
    url.strip() for url in open("munro_urls.txt").read().split("\n") if url
]

file = open("munro_data.json", "a")

munros_data_object = {}

for domain in munro_domains:
    munro_data = {}
    page_content = requests.get(domain).text

    soup = BeautifulSoup(page_content, features="html.parser")

    # Munro Name
    name = soup.find("h1").find("span").text.strip()
    print(name)
    munro_data["name"] = name

    # Munro Height
    altitude_string = soup.select_one('p:-soup-contains("Altitude")').text.strip()
    altitude_string = altitude_string[len("Altitude: ") :].strip()
    altitude_string = altitude_string.removesuffix(" metres")
    print(altitude_string)
    munro_data["altitude"] = altitude_string

    # Munro Region
    region_string = soup.select_one('p:-soup-contains("Region")').find("a").text
    print(region_string)
    munro_data["region"] = region_string

    # Munro Rating
    rating = soup.find("strong").text.strip()
    print(rating)
    munro_data["rating"] = rating

    # Munro Route
    munro_data["routes"] = []
    routes_heading = soup.select_one('h2:-soup-contains("Detailed route")')
    routes = routes_heading.find_next_sibling().find_all("a")
    for link in routes:
        route_path = link.get("href")
        route_domain = f"https://www.walkhighlands.co.uk{route_path}"
        print(route_domain)
        munro_data["routes"].append(route_domain)

    # Munro Description
    description = soup.find_all("b")[2].text.strip()
    print(description)
    munro_data["description"] = description

    # Munro Number of Climbers
    number_of_climbers = soup.select_one(
        'a:-soup-contains("Walkhighlanders")'
    ).text.strip()
    number_of_climbers = number_of_climbers.removesuffix(" Walkhighlanders")
    print(number_of_climbers)
    munro_data["number_of_climbers"] = number_of_climbers

    unique_name = domain.rsplit("/", 1)[-1]
    munros_data_object[unique_name] = munro_data

json.dump(munros_data_object, file, indent=4, sort_keys=True)
file.close()
