
import json
from datetime import datetime

INPUT_FILE = "data/data.json"
OUTPUT_FILE = "data/transform.json"

def transform_data(raw_text):
    lines = raw_text.strip().splitlines()
    result = {"date": None, "cities": []}

    current_city = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("ngay:"):
            date_str = line.split(":", 1)[1].strip()
            result["date"] = datetime.strptime(date_str, "%d/%m/%Y").date().isoformat()

        elif line.startswith("tinh:"):
            if current_city:
                result["cities"].append(current_city)
            city_name = line.split(":", 1)[1].strip()
            current_city = {
                "name": city_name,
                "matinh": "",
                "prizes": {}
            }
        elif line.startswith("matinh:"):
            if current_city:
                current_city["matinh"] = line.split(":", 1)[1].strip()

        elif line.startswith("giai"):
            if current_city:
                key, val = line.split(":", 1)
                numbers = [x.strip() for x in val.split(",") if x.strip()]
                current_city["prizes"][key] = numbers

    if current_city:
        result["cities"].append(current_city)

    return result

if __name__ == "__main__":
    transform_datas = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        datas = json.load(f)
    extract_datas = datas.get('extract_data')
    for text in extract_datas:
        transform_datas.append(transform_data(text))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(transform_datas, f, ensure_ascii=False, indent=2)