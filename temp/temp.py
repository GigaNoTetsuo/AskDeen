import csv
import json

# Input and output paths
input_file = "/home/nebulamind/Documents/AI Lab/AskDeen/Para30_tags.csv"
output_file = "output.jsonl"

with open(input_file, "r", encoding="utf-8") as csvfile, open(output_file, "w", encoding="utf-8") as jsonlfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        # Extract tags and clean
        tags = [tag.strip() for tag in row["tag_2"].strip('"').split(",")]

        # Create JSONL row
        data = {
            "surah_ayah": row["ID"].strip(),
            "translation": row["TRANSLATION"].strip(";"),
            "tag1": tags[0] if len(tags) > 0 else "",
            "tag2": tags[1] if len(tags) > 1 else ""
        }
        jsonlfile.write(json.dumps(data, ensure_ascii=False) + "\n")
