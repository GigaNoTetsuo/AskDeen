import os
import json
import pandas as pd
from typing import Dict

# Paths
PREPARED_DIR = "/home/nebulamind/Documents/AI Lab/AskDeen/translation_batches_500"
os.makedirs(PREPARED_DIR, exist_ok=True)
BATCH_SIZE = 6236
MODEL_NAME = "meta-llama/llama-4-maverick-17b-128e-instruct" 
gpt_model = "gpt-4.1-2025-04-14"

#--------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def create_optimized_prompt(context_data: dict) -> str:
    """Create a balanced prompt for Quranic verse tag generation (1000-1100 words)"""

    prompt = """Generate 2 conceptual tags that capture the core semantic themes of the given Quranic verse.
    Tags must be semantically rich, contextually accurate, and user-focused.

CONTEXT VERSES:
"""


    # Add context verses
    # for row in context_data["context_rows"]:
    #     marker = ">>> TARGET VERSE (Generate tags for this) <<<" if row["is_target"] else ""
    #     prompt += f"Verse ID: {row['id']} {marker}\n"
    #     prompt += f"Translation: {row['translation']}\n\n"
    target_index = None
    for i, row in enumerate(context_data["context_rows"]):
      if row["is_target"]:
          target_index = i
          break

    if target_index is not None:
      # Get previous, target, and next verses
      previous_verse2 = context_data["context_rows"][target_index - 2] if target_index-1 > 0 else None
      previous_verse1 = context_data["context_rows"][target_index - 1] if target_index > 0 else None

      target_verse = context_data["context_rows"][target_index]
      next_verse1 = context_data["context_rows"][target_index + 1] if target_index < len(context_data["context_rows"])-1 else None
      next_verse2 = context_data["context_rows"][target_index + 2] if target_index < len(context_data["context_rows"])-2 else None

    # Build the new prompt format
      if previous_verse1:
          print("P1 done")
          prompt += f"*Previous1:* {previous_verse1['translation']}\n"
      if previous_verse2:
          prompt += f"*Previous2:* {previous_verse2['translation']}\n"

      prompt += f"*TARGET:* {target_verse['translation']}\n"
      if next_verse1:
          prompt += f"*Next1:* {next_verse1['translation']}\n"
      if next_verse2:
          prompt += f"*Next2:* {next_verse2['translation']}\n"

    prompt += """ ## Focus
- What is this verse fundamentally about?
- What are the main concepts and themes present?
- What theological/spiritual/moral domains does it address?

## Conceptual Tag Categories
1. **About Allah**: allah-names, allah-mercy, allah-power, divine-love, allah-forgiveness
2. **About Prophets**: prophet-stories, prophet-teachings, messenger-guidance, prophetic-examples
3. **Prayer & Worship**: salah-guidance, dua-supplications, dhikr-remembrance, worship-methods, spiritual-connection
4. **Good Character**: honesty-truth, kindness-compassion, patience-perseverance, humility-modesty, gratitude-thankfulness
5. **Family & Relationships**: parent-respect, marriage-love, children-upbringing, family-harmony, social-bonds
6. **Daily Life Guidance**: halal-haram, life-decisions, problem-solving, personal-growth, righteous-living
7. **Charity & Helping**: zakat-sadaqah, helping-needy, community-care, generosity-giving, social-responsibility
8. **Afterlife & Judgment**: paradise-heaven, hell-warning, day-judgment, life-after-death, divine-justice

## Guidelines
- Use 2-3 words maximum per tag
- Focus on abstract concepts rather than specific practices
- Think semantically, not functionally
- Avoid overlapping with practical applications

## Output Format:
{
    "verse": "verse text",
    "conceptual_tags": ["concept-1", "concept-1"]
}
"""

    return prompt


def get_contextual_rows(df: pd.DataFrame, current_index: int) -> Dict:
        """Get context rows (3 above and 3 below current row)"""
        start_idx = max(0, current_index - 3)
        end_idx = min(len(df), current_index + 3 + 1)

        context_rows = []
        target_row = None

        for i in range(start_idx, end_idx):
            # Assuming your CSV has columns 'ID' and 'Abdullah Yusuf Ali'
            row_data = {
                "id": str(df.iloc[i]['ID']),
                "translation": str(df.iloc[i]['Abdullah Yusuf Ali'])
            }

            if i == current_index:
                target_row = row_data
                row_data["is_target"] = True
            else:
                row_data["is_target"] = False

            context_rows.append(row_data)

        return {
            "context_rows": context_rows,
            "target_row": target_row
        }
#-------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------

# Load dataset
df = pd.read_excel("/home/nebulamind/Documents/AI Lab/AskDeen/dataset/Translation File.xlsx")  

# Output JSONL file
total_rows = len(df)

# Split into batches
batch_count = (total_rows + BATCH_SIZE - 1) // BATCH_SIZE

for batch_index in range(batch_count):
    start_idx = batch_index * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, total_rows)

    output_filename = f"gpt_batch_complete_{batch_index + 1:03}.jsonl"
    output_path = os.path.join(PREPARED_DIR, output_filename)

    with open(output_path, "w", encoding="utf-8") as fout:
        for idx in range(start_idx, end_idx):
            print(f"📍 Processing row {idx + 1}/{total_rows} (ID: {df.iloc[idx]['ID']})")

            try:
                context = get_contextual_rows(df=df, current_index=idx)
                prompt = create_optimized_prompt(context)

                request = {
                    "custom_id": f"Verse: {df.iloc[idx]['ID']}",
                    # "method": "POST",
                    # "url": "/v1/chat/completions",
                    # "body": {
                    #     "model": gpt_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert in Quranic understanding, theology, and conceptual theme extraction."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        # "max_tokens": 200,
                        # "temperature": 0.3
                    # }
                }

                fout.write(json.dumps(request, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"❌ Error at row {idx}: {e}")

    print(f"✅ Saved batch {batch_index + 1} → {output_path}")

print("\n🎉 All batches created successfully!")