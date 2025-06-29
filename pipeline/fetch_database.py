import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

OUTPUT_FILE = "data/data.json"

def format_data(datas):
    result = {
        "table_html": [],
        "date_crawl": [],
        "extract_data": []
    }
    for data in datas:
        result["table_html"].append(data['raw_data'])
        result["extract_data"].append(data['extract_data'])
        result["date_crawl"].append(data['crawl_date'].strftime("%Y-%m-%d %H:%M:%S"))
    return result

def fetch_database():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        port=os.environ.get("DB_PORT", 5432)
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM raw")

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            results = [dict(zip(columns, row)) for row in rows]

            cur.execute("""
                DROP TABLE lottery_result;
                DROP TABLE lottery_draw;
                DROP TABLE raw;
            """)

            return format_data(results)

    conn.commit()
    cur.close()
    conn.close()

    return datas

if __name__ == "__main__":
    datas = fetch_database()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(datas, f, ensure_ascii=False, indent=2)