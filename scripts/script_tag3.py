import csv
import json

input_csv = "/home/nebulamind/Documents/AI Lab/AskDeen/dataset/Para30_tags_updated.csv"
output_json = "/home/nebulamind/Documents/AI Lab/AskDeen/dataset/para_30_updated_tags.json"

data = []

with open(input_csv, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tag2 = row['tag_2'].strip('" ')
        tags = [t.strip() for t in tag2.split(',')]

        entry = {
            "id": row["ID"].strip(),
            "translation": row["TRANSLATION"].strip(),
            "t1": tags[0] if len(tags) > 0 else None,
            "t2": tags[1] if len(tags) > 1 else None
        }

        data.append(entry)

with open(output_json, mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=2, ensure_ascii=False)

print(f"✅ Converted {input_csv} → {output_json}")
