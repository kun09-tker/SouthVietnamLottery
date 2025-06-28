import json
import requests

from datetime import datetime
from bs4 import BeautifulSoup

OUTPUT_FILE = "data/data.json"
URL = "https://www.minhngoc.net.vn/ket-qua-xo-so/mien-nam.html"

def crawl_data():
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
        'table_html': [table],
        'date_crawl': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    crawl_data()