import os
import json
import psycopg2
from dotenv import load_dotenv

INPUT_RAW_FILE = "data/data.json"
INPUT_TRANSFORM_FILE = "data/transform.json"

load_dotenv()

def load_data(raw_data, transform_data):
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
                CREATE TABLE IF NOT EXISTS raw (
                    id SERIAL PRIMARY KEY,
                    raw_data TEXT,
                    crawl_date TIMESTAMP,
                    extract_data TEXT
                );

                CREATE TABLE IF NOT EXISTS lottery_draw (
                    id SERIAL PRIMARY KEY,
                    raw_id INTEGER REFERENCES raw(id),
                    draw_date DATE
                );

                CREATE TABLE IF NOT EXISTS lottery_result (
                    id SERIAL PRIMARY KEY,
                    draw_id INTEGER REFERENCES lottery_draw(id),
                    city_name TEXT,
                    code TEXT,
                    prize_level TEXT,
                    numbers TEXT[]
                );
            """)

            cur.execute(
                "INSERT INTO raw (raw_data, crawl_date, extract_data) VALUES (%s, %s, %s)",
                (raw_data.get('table_html'), raw_data.get('date_crawl'), raw_data.get('extract_data'))
            )
            cur.execute(
                "SELECT id FROM raw WHERE crawl_date = %s",
                (raw_data.get('date_crawl'),)
            )

            raw_id = cur.fetchone()[0]
            date = transform_data.get('date')
            cur.execute(
                "INSERT INTO lottery_draw (raw_id, draw_date) VALUES (%s, %s)",
                (raw_id, date)
            )
            cur.execute(
                "SELECT id FROM lottery_draw WHERE draw_date = %s",
                (date,)
            )

            draw_id = cur.fetchone()[0]
            for city_result in transform_data.get("cities"):
                city_name = city_result.get("name")
                code = city_result.get("matinh")

                for prize in ["giai8","giai7","giai6","giai5","giai4","giai3","giai2","giai1","giaidb"]:
                    numbers = None
                    numbers = city_result.get('prizes').get(prize, [])
                    cur.execute(
                        """
                        INSERT INTO lottery_result (draw_id, city_name, code, prize_level, numbers)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (draw_id, city_name, code, prize, numbers)
                    )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    with open(INPUT_RAW_FILE, encoding="utf-8") as f:
        raw_datas = json.load(f)
    with open(INPUT_TRANSFORM_FILE, encoding="utf-8") as f:
        transform_datas = json.load(f)
    reshape_raw_datas = [dict(zip(raw_datas.keys(), values)) for values in zip(*raw_datas.values())]

    for raw_data, transfrom_data in zip(reshape_raw_datas, transform_datas):
        load_data(raw_data, transfrom_data)