import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.amazon.in/s"
search_term = "bags"
pages = 40

data = []

for page in range(1, pages + 1):
    params = {
        "k": search_term,
        "crid": "2M096C61O4MLT",
        "qid": 1653308124,
        "sprefix": "ba,aps,283",
        "ref": f"sr_pg_{page}",
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in products:
        p = {}

        url_ele = product.find("a", class_="a-link-normal")
        p["URL"] = "https://www.amazon.in" + url_ele["href"] if url_ele else "Not available"

        name = product.find("span", class_="a-size-medium")
        p["Name"] = name.text.strip() if name else "Not available"

        price= product.find("span", class_="a-offscreen")
        p["Price"] = price.text.strip() if price else "Not available"

        rating = product.find("span", class_="a-icon-alt")
        p["Rating"] = rating.text.strip() if rating else "Not available"

        reviews = product.find("span", class_="a-size-base")
        p["Reviews"] = reviews.text.strip() if reviews else "Not available"

        data.append(p)

for p in data:
    response = requests.get(p["URL"])
    soup = BeautifulSoup(response.content, "html.parser")

    p["Desc"] = "Not available"
    p["ASIN"] = "Not available"
    p["ProdDesc"] = "Not available"
    p["Manufacturer"] = "Not available"

keys = ["URL", "Name", "Price", "Rating", "Reviews", "Desc", "ASIN", "ProdDesc", "Manufacturer"]

with open("assignment.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
