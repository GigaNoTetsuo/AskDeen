import json
import re

input_file = "/home/nebulamind/Documents/AI Lab/tags_generator/output3.txt"
output_file = "output_3.json"

data = []

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if "Missing required keys in response:" in line:
        try:
            # Extract the JSON-like dictionary from the line
            match = re.search(r"Missing required keys in response: (.*)", line)
            if not match:
                continue
            dict_str = match.group(1)
            parsed = eval(dict_str)  # Safe here since input is controlled

            verse = parsed.get("verse", "").strip()
            tags = parsed.get("conceptual_tags", [])
            tag1 = tags[0] if len(tags) > 0 else ""
            tag2 = tags[1] if len(tags) > 1 else ""

            data.append({
                "verse": verse,
                "tag1": tag1,
                "tag2": tag2
            })

        except Exception as e:
            print(f"Error parsing line: {line}\n{e}")

# Write to JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Converted {len(data)} entries to {output_file}")
