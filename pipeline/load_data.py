
import os
import json
import psycopg2
from datetime import datetime
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
                    extract_data JSONB
                );

                CREATE TABLE IF NOT EXISTS lottery_draw (
                    id SERIAL PRIMARY KEY,
                    raw_id INTEGER REFERENCES raw(id),
                    draw_date DATE UNIQUE
                );

                CREATE TABLE IF NOT EXISTS lottery_result (
                    id SERIAL PRIMARY KEY,
                    draw_id INTEGER REFERENCES lottery_draw(id),
                    city TEXT,
                    code TEXT,
                    prize_level TEXT,
                    numbers TEXT[]
                );
            """)

            cur.execute(
                "INSERT INTO raw (raw_data, extract_data) VALUES (%s, %s)",
                (raw_data.get('table_html'), json.dumps(raw_data.get('extract_data')))
            )
            cur.execute(
                "SELECT id FROM raw WHERE raw_data = %s",
                (raw_data.get('table_html'),)
            )

            raw_id = cur.fetchone()[0]
            date_str = transform_data.get('date')
            date = datetime.strptime(date_str, '%d/%m/%Y').date()
            cur.execute(
                "INSERT INTO lottery_draw (raw_id, draw_date) VALUES (%s, %s)",
                (raw_id, date)
            )
            cur.execute(
                "SELECT id FROM lottery_draw WHERE draw_date = %s",
                (date,)
            )

            draw_id = cur.fetchone()[0]
            for city_result in transform_data.get("results"):
                city = city_result.get("city")
                code = city_result.get("code")

                for prize in ["giai8","giai7","giai6","giai5","giai4","giai3","giai2","giai1","giaidb"]:
                    numbers = None
                    numbers = city_result.get(prize, [])
                    cur.execute(
                        """
                        INSERT INTO lottery_result (draw_id, city, code, prize_level, numbers)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (draw_id, city, code, prize, numbers)
                    )

    conn.close()

if __name__ == "__main__":
    with open(INPUT_RAW_FILE, encoding="utf-8") as f:
        raw_data = json.load(f)
    with open(INPUT_TRANSFORM_FILE, encoding="utf-8") as f:
        transform_data = json.load(f)

    load_data(raw_data, transform_data)