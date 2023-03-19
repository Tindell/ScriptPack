# gpt 3.5 solution, with some modification

import pyperclip
import openai
import os
import math
# Function to interact with OpenAI API
def process_clipboard_content(clipboard_content):
    print("Processing text")
    system_prompt = select_a_prompt()
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": clipboard_content},
    ]
    leng = select_a_length(len(clipboard_content))

    if(leng > 2000):
        leng = 2000

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=leng,
        n=1,
        temperature=0.5,
    )
    # Get the assistant's reply from the response
    assistant_reply = response.choices[0].message.content

    return assistant_reply.strip()

def select_a_prompt():    
    system_prompts = {
        "Simplify copied python code": "Simplify the following python code.  Return only the new python code, with no explaination.",
        "Summerize copied text ": "Generate a summary for the following text:",
    }
    print("Please choose a system prompt:")
    for index, prompt_name in enumerate(system_prompts.keys(), start=1):
        print(f"{index}: {prompt_name}")
    choice = int(input("Enter the prompt number: "))
    return list(system_prompts.values())[choice - 1]

def select_a_length(num_letters):
    # Print the list of system prompt names for the user to choose from
    print(f"How any tokens should I reply with? You sent me roughly {math.ceil(num_letters/4)} tokens")
    return int(input())

def main():
    clipboard_text = pyperclip.paste()

    modified_text = process_clipboard_content(clipboard_text)

    pyperclip.copy(modified_text)

    print("Modified text:", modified_text)

if __name__ == "__main__":
    main()