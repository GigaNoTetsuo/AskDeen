import csv
import json
import ast

input_csv = '/home/nebulamind/Documents/AI Lab/AskDeen/outputs/output_Surah123.csv'   # Replace with your CSV filename
output_json = '/home/nebulamind/Documents/AI Lab/AskDeen/outputs/json_Surah123.json'

data = []

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Parse the tag_2 column which looks like a list in string form
        tags = []
        if row['tag_2']:
            try:
                tags = ast.literal_eval(row['tag_2'])
            except:
                tags = []

        # Prepare dictionary for output
        record = {
            'ID': row['ID'],
            'Translation': row['Abdullah Yusuf Ali'],
            'Tag1': tags[0] if len(tags) > 0 else None,
            'Tag2': tags[1] if len(tags) > 1 else None,
        }
        data.append(record)

# Write JSON output
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

print(f"Converted {len(data)} records to {output_json}")
