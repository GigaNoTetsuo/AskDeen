import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


client = Groq(api_key="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")
client1 = OpenAI(api_key="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")

# file_path = "/home/nebulamind/Documents/AI Lab/AskDeen/prepared_outputs/verse_tagging_batch_001.jsonl"
# response = client1.files.create(file=open(file_path, "rb"), purpose="batch")
# print(response)


job_ids = ["file-JueNqzagVH4e7FiYoGKV3Z"]


OUTPUT_DIR = "./outputs_groq"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_outputs():
    all_data = []

    for job_id in job_ids:
        print(f"📥 Fetching job {job_id}")
        batch = client.batches.retrieve(job_id)
        file_id = batch.output_file_id

        if not file_id:
            print(f"⚠️ No output file yet for job {job_id}")
            continue

        content = client.files.content(file_id).text
        with open(f"{OUTPUT_DIR}/{job_id}_output.jsonl", "w", encoding="utf-8") as f:
            f.write(content)

        for line in content.strip().split("\n"):
            record = json.loads(line)
            custom_id = record["custom_id"]
            translated = record["response"]["body"]["choices"][0]["message"]["content"]
            all_data.append({"custom_id": custom_id, "translation": translated})

    df = pd.DataFrame(all_data)
    df.to_csv(f"{OUTPUT_DIR}/all_translations.csv", index=False)
    print("✅ Results saved to all_translations.csv")

if __name__ == "__main__":
    download_outputs()