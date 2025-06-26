import os
import psycopg2
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

def fetch_clock():
    url = "https://time.is/vi/"
    headers = {
        "User-Agent": "Mozilla/5.0"  # để tránh bị chặn
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    clock_div = soup.find("div", id="clock0_bg")
    return clock_div.prettify() if clock_div else None

def save_to_postgres(data_html):
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        port=os.environ.get("DB_PORT", 5432)
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS timeis_html (
                    id SERIAL PRIMARY KEY,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    content TEXT
                );
            """)
            cur.execute("INSERT INTO timeis_html (content) VALUES (%s);", (data_html,))
    conn.close()

if __name__ == "__main__":
    html = fetch_clock()
    if html:
        save_to_postgres(html)
        print("✅ Clock data saved.")
    else:
        print("⚠️ Clock div not found.")