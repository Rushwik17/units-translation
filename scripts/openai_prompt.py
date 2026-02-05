import sys
import os
import random
import time
from openai import OpenAI


input_words_file = "../data_ver3/metric_units.txt"
output_dir = "../samples2"
api_key = ""

client = OpenAI(
    api_key=api_key
)

MODEL_ID = "gpt-4o-mini"  
# Alternatives:
# "gpt-4.1"
# "gpt-4o-mini" (fast, cheaper)

MAX_RETRIES = 5
BASE_DELAY = 2.0


PROMPT_TEMPLATE = """
You are given a measurement unit name that may include its symbol.
Ignore the symbol and focus only on the unit name.

Output exactly one sentence as plain text. Do not add explanations.

Requirements:
The sentence :
- Should not be too small, containing atleast 20 words.
- It should look like a part or a dialogue, article or a textbook.
- Use the word's plural form when necessary.
- The word should be used in the sentence to measure something.
- You are also allowed to use numericals/decimals along with the units.
- You are free to use a random name for more colloquial nature.

Unit:
{sentence}
"""


with open(input_words_file, "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]


os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, os.path.basename(input_words_file))


with open(output_file, "w", encoding="utf-8") as fo:
    for idx, sentence in enumerate(words, start=1):

        prompt = PROMPT_TEMPLATE.format(sentence=sentence)

        for attempt in range(MAX_RETRIES):
            try:
                time.sleep(1.0)

                response = client.chat.completions.create(
                    model=MODEL_ID,
                    messages=[
                        {"role": "system", "content": "You are a precise language generator."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=1.0,
                    max_tokens=256,
                )

                if response.choices:
                    text = response.choices[0].message.content
                    if text and text.strip():
                        generated_sentence = " ".join(text.strip().split())
                        fo.write(generated_sentence + "\n")
                        fo.flush()
                        print(f"[{idx}/{len(words)}] Success: {sentence}")
                        break

                print(f"[{idx}/{len(words)}] Empty response for '{sentence}'. Retrying...")
                time.sleep(BASE_DELAY)

            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    wait_time = BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(
                        f"[{idx}] Rate limit hit. "
                        f"Attempt {attempt + 1}/{MAX_RETRIES}. "
                        f"Waiting {wait_time:.2f}s..."
                    )
                    time.sleep(wait_time)
                else:
                    print(f"[{idx}] Permanent error for '{sentence}': {e}")
                    break
        else:
            print(f"[{idx}] FAILED after {MAX_RETRIES} attempts: {sentence}")

print(f"\nDone. Output saved to {output_file}")
