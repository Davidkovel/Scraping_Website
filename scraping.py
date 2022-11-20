import requests
from bs4 import BeautifulSoup
import csv

CSV = "laptops.csv"
url = "https://www.olx.ua/d/uk/elektronika/noutbuki-i-aksesuary/"
headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0"
    }
# bot check
def get_data(url, params=''):
    req = requests.get(url, headers=headers, params=params)
    return req
def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="css-qfzx1y")
    laptops = []

    for item in items:
        laptops.append({
            'title': item.find('h6', class_="css-1pvd0aj-Text eu5v0x0").get_text(strip=True),
            'price': item.find('p', class_="css-1q7gvpp-Text eu5v0x0").get_text(strip=True),
            'city': item.find('p', class_="css-p6wsjo-Text eu5v0x0").get_text(strip=True),
            })

    return laptops
    # global laptop
    # for laptop in laptops:
    #     print(f"{laptop['title']} : {laptop['price']} : {laptop['city']} - {laptop['link_href']}")

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Название", "Цена", "Город"])
        for item in items:
            writer.writerow([item["title"], item["price"], item["city"]])


def parsing_page():
    print("Enter the page that you want to parsing")
    pagenation = int(input("Enter Page: "))
    html = get_data(url)
    if html.status_code == 200:
        laptops = []
        for page in range(1, pagenation+1):
            print(f"Enter Page {page}")
            html = get_data(url, params={'page': page})
            laptops.extend(get_content(html.text))
            save_doc(laptops, CSV)
        print("Parsing finished")
    else:
        print("Error")


parsing_page()
