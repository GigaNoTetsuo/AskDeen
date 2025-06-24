import csv
import json

# Input and output file paths
csv_file = "/home/nebulamind/Documents/AI Lab/tags_generator/test_out.csv"
json_file = "output.json"

# List to store JSON data
json_data = []

# Read and convert
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Split tag columns by comma and strip spaces
        tag2 = [tag.strip() for tag in row['tag_2'].split(',')]
        tag3 = [tag.strip() for tag in row['tag_3'].split(',')]

        # Build JSON object
        json_data.append({
            "id": row["ID"],
            "translation": row["Translation"],
            "p1": tag2[0] if len(tag2) > 0 else "",
            "p2": tag2[1] if len(tag2) > 1 else "",
            "s1": tag3[0] if len(tag3) > 0 else "",
            "s2": tag3[1] if len(tag3) > 1 else ""
        })

# Save to JSON file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print("JSON conversion complete.")
