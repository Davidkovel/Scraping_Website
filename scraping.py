import requests
from bs4 import BeautifulSoup
import csv
import time


CSV = "laptops.csv"
url = "https://answear.ua/k/vona/odyag/bluzki"
host = 'https://answear.ua'
headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
    }

def get_data(url, params=''):
    req = requests.get(url, headers=headers, params=params)
    return req

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_='m-4 l-3 Products__productsFullWide__mix1Y xs-6')
    # images = soup.find_all("img")
    laptops = []

    for item in items:
        ttl = item.find('div', class_ = "ProductItem__productCardName__DCKIH").get_text(strip=True)
        prc = item.find('div', class_='Price__salePrice__FCFFF ProductItem__priceSale__XP3ik')
        if prc is not None:
            prc = prc.get_text(strip=True)
            laptops.append({
                'title': ttl,
                'price': prc,
                'imagee': item.find('picture', class_='Image__cardImage__xvgs1').find('img').get('src'),
                'get_link': host + item.find('a').get('href')
             })
    return laptops


def save_doc(items, path):
    with open(path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Название", "Цена", "Картинка", "Сылка на продукт"])
        for item in items:
            writer.writerow([item["title"], item["price"], item['imagee'], item['get_link']])


def parsing_page():
    print("Enter the page that you want to parsing")
    pagenation = int(input("Enter Page: "))
    html = get_data(url)
    if html.status_code == 200:
        laptops = []
        for page in range(1, pagenation+1):
            print(f"Enter Page {page}")
            html = get_data(url, params={'page': page})
            time.sleep(2)
            laptops.extend(get_content(html.text))
        save_doc(laptops, CSV)
        print("Parsing finished")
    else:
        print("Error")


parsing_page()
