
import json

INPUT_FILE = "data/data.json"
OUTPUT_FILE = "data/transform.json"

def transform_data(parsed_data):
    return parsed_data.get('extract_data')

if __name__ == "__main__":
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    data = transform_data(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)