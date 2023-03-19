# gpt 3.5 solution, with some modification

import pyperclip
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = "Generate a summary for the following text:"

clipboard_text = pyperclip.paste()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": clipboard_text},
]

response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            n=1,
            temperature=0.5,
        )

modified_text = response.choices[0].message.content.strip()

pyperclip.copy(modified_text)

print("Modified text:", modified_text)