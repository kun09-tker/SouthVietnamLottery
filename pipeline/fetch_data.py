import json
import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = "data/data.json"
URL = "https://www.minhngoc.net.vn/ket-qua-xo-so/mien-nam.html"

def fetch_data():
    table = None
    print(f"Fetching {URL} ...")
    headers = {
        "User-Agent": "Mozilla/5.0"  # để tránh bị chặn
    }
    response = requests.get(URL, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    table_bkqmiennam = soup.find("table", class_="bkqmiennam")
    if table_bkqmiennam:
        table = table_bkqmiennam.prettify()
    data = {
        'table_html': table
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_data()