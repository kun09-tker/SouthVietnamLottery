import json
from bs4 import BeautifulSoup

INPUT_FILE = "data/data.json"
OUTPUT_FILE = "data/data.json"

def extract_lottery_info(html: str):
    msg = ""
    soup = BeautifulSoup(html, 'html.parser')
    ngay = soup.select_one('td.ngay a').text.strip()
    msg += f"ngay:{ngay}\n"

    for table in soup.select('table.rightcl'):
        tinh = table.select_one('td.tinh').text.strip()
        matinh = table.select_one('td.matinh').text.strip()
        msg += f"tinh:{tinh}\n"
        msg += f"matinh:{matinh}\n"

        for giai in ["giai8","giai7","giai6","giai5","giai4","giai3","giai2","giai1","giaidb"]:
            cells = table.select(f"td.{giai} div")
            numbers = [c.text.strip() for c in cells]
            if numbers:
                msg += f"{giai}:{','.join(numbers)}\n"
    return msg

if __name__ == "__main__":
    with open(INPUT_FILE, encoding="utf-8") as f:
        datas = json.load(f)
    table_htmls = datas.get("table_html")
    strings = []
    for html in table_htmls:
        parsed = extract_lottery_info(html)
        strings.append(parsed)

    datas['extract_data'] = strings

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(datas, f, ensure_ascii=False, indent=2)

    print(f"✅ Extracted data saved to {OUTPUT_FILE}")