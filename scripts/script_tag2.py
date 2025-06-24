import json
import re

input_tag_file = "/home/nebulamind/Documents/AI Lab/tags_generator/output3.txt"
# Read the log-style file
with open(input_tag_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

data = []
current_id = None

for line in lines:
    # Extract ID from "Processing row"
    if "Processing row" in line:
        match = re.search(r'ID: ([\d\|]+)', line)
        if match:
            current_id = match.group(1).strip()

    # Extract tag dictionary
    elif "✓ Generated tags:" in line:
        # Find the JSON-like dictionary string
        tag_dict_match = re.search(r"\{.*\}", line)
        if tag_dict_match:
            tag_entry = eval(tag_dict_match.group())  # Safe here due to controlled format

            target_verse = tag_entry["Target Verse"]
            primary_tags = [tag.strip() for tag in tag_entry["Primary"].split(",")]
            secondary_tags = [tag.strip() for tag in tag_entry["Secondary"].split(",")]

            # Build structured output
            data.append({
                "id": current_id,
                "translation": target_verse,
                "p1": primary_tags[0] if len(primary_tags) > 0 else "",
                "p2": primary_tags[1] if len(primary_tags) > 1 else "",
                "s1": secondary_tags[0] if len(secondary_tags) > 0 else "",
                "s2": secondary_tags[1] if len(secondary_tags) > 1 else ""
            })

# Save to JSON
with open("structured_tags.json", "w", encoding="utf-8") as out_file:
    json.dump(data, out_file, indent=2, ensure_ascii=False)

print("✅ Conversion complete. Saved to structured_tags.json")
