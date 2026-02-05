import sys
import os
import random
from google import genai
from google.genai import types
import time

input_words_file = "../data_ver3/metric_units.txt"
output_dir = "../samples2"
api_key = ""

client = genai.Client(
    api_key=api_key,
)

model_id = "models/gemini-3-pro-preview"

config = types.GenerateContentConfig(
    temperature=1,
    max_output_tokens=1024,
)

PROMPT_TEMPLATE = """
You are given a measurement unit name that may include its symbol.
Ignore the symbol and focus only on the unit name.
Output exactly one sentences as plain text. Do not add explanations, lists, or formatting.

The sentence :
- Should not be too small, containing atleast 20 words.
- It should look like a part or a dialogue, article or a textbook.
- Use the word's plural form when necessary.
- The word should be used in the sentence to measure something.
- You are also allowed to use numericals/decimals/fractions along with the units.
- You are free to use a random name for more colloquial nature.

The sentence:
{sentence}
"""

try:
    with open(input_words_file, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
except Exception as e:
    print(f"Critical Error: File not found or unreadable. {e}")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, os.path.basename(input_words_file))

with open(output_file, "w", encoding="utf-8") as fo:
    for idx, sentence in enumerate(words, start=1):
        max_retries = 5
        base_delay = 2.0

        prompt = PROMPT_TEMPLATE.format(sentence=sentence)

        for attempt in range(max_retries):
            try:
                time.sleep(1.0) 

                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=config
                )

                if response and response.text:
                    generated_sentence = " ".join(response.text.strip().split())
                    fo.write(f"{generated_sentence}\n")
                    fo.flush()
                    print(f"[{idx}/{len(words)}] Success: {sentence}")
                    break 
                else:
                    print(f"[{idx}/{len(words)}] Empty response for '{sentence}'. Retrying...")
                    time.sleep(base_delay)

            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"[{idx}] Rate limit hit. Attempt {attempt+1}/{max_retries}. Waiting {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    print(f"[{idx}] Permanent error for '{sentence}': {e}")
                    break 
        else:
            print(f"[{idx}] FAILED after {max_retries} attempts: {sentence}")

print(f"\nDone. Output saved to {output_file}")