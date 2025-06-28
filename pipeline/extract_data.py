import json
from bs4 import BeautifulSoup

INPUT_FILE = "data/data.json"
OUTPUT_FILE = "data/data.json"

def extract_lottery_info(html: str):
    soup = BeautifulSoup(html, "html.parser")

    date_tag = soup.select_one("td.ngay a")
    date = date_tag.get_text(strip=True) if date_tag else None

    tables = soup.select("table.rightcl")
    all_results = []

    for table in tables:
        result = {}

        tinh = table.select_one("td.tinh")
        result["city"] = tinh.get_text(strip=True) if tinh else None

        for giai in ["giai8", "giai7", "giai6", "giai5", "giai4", "giai3", "giai2", "giai1", "giaidb"]:
            td = table.select_one(f"td.{giai}")
            if td:
                divs = td.find_all("div")
                if divs:
                    result[giai] = [d.get_text(strip=True) for d in divs]
                else:
                    result[giai] = [td.get_text(strip=True)]
            else:
                result[giai] = []

        all_results.append(result)

    return {
        "date": date,
        "results": all_results
    }

if __name__ == "__main__":
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    table_html = data.get("table_html")
    parsed = extract_lottery_info(table_html)
    data['extract_data'] = parsed

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Extracted data saved to {OUTPUT_FILE}")