import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
# Replace with your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Endpoint and model
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-4-maverick-17b-128e-instruct"  # LLaMA 4 Maverick (use exact model name as in Groq docs)

# Headers
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Example prompts
prompts = [
    "What is quantum computing?",
    "Explain photosynthesis in simple terms.",
    "How does the stock market work?",
    "Tell me a joke about programmers.",
    "Summarize the causes of World War I.",
    # Add more prompts as needed
]

# Batch size
batch_size = 5

# Function to call Groq API
def call_groq_batch(batch):
    results = []
    for prompt in batch:
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            generated_text = data['choices'][0]['message']['content']
            results.append((prompt, generated_text))
        else:
            print("Error:", response.status_code, response.text)
            results.append((prompt, None))
        time.sleep(0.1)  # Be kind to the API
    return results

# Process prompts in batches
for i in range(0, len(prompts), batch_size):
    batch = prompts[i:i+batch_size]
    outputs = call_groq_batch(batch)
    for input_text, output_text in outputs:
        print(f"Prompt: {input_text}\nResponse: {output_text}\n{'-'*50}")
