import json

# Input and output file paths
input_file = "/home/nebulamind/Documents/AI Lab/AskDeen/prepared_outputs/gpt_batch_001.jsonl"
output_file = "/home/nebulamind/Documents/AI Lab/AskDeen/prepared_outputs/gpt_batch_test.jsonl"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        data = json.loads(line)
        
        # Extract the messages from the original structure
        try:
            messages = data["body"]["messages"]
            simplified = {"messages": messages}
            outfile.write(json.dumps(simplified, ensure_ascii=False) + "\n")
        except KeyError as e:
            print(f"Skipping line due to missing key: {e}")
