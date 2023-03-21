import openai
import os
import math
import json
from src.openaiinteractions import OpenAIInteraction

class PromptPrompt(OpenAIInteraction):
    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)

    def save_response(self, role, content, filename="saved_prompts.json"):
        data = []

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)

        data.append({"role": role, "content": content})

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)


def main():
    sing = PromptPrompt()
    up = input("Enter a user prompt: ")
    rt = int(input("How many response tokens? "))
    sp = "You are now a system prompt writer. Your task is to provide comprehensive prompts for ChatGPT to respond to user requests. Your prompts should be clear, concise, and provide all necessary information for ChatGPT to understand the user's request and provide an appropriate response. You should also consider any potential errors or misunderstandings that may arise and provide suggestions for correcting them.  When writing your prompts, be sure to use clear and concise language, and provide examples when necessary. Consider the context of the user's request and provide relevant information that may be needed to provide an accurate response.  You should also consider the potential limitations of ChatGPT and provide prompts that are within its capabilities."
    messages = [
        {"role": "system", "content": sp},
    ]

    if os.path.exists("saved_prompts.json"):
        with open("saved_prompts.json", 'r') as file:
            saved_prompts = json.load(file)
            messages.extend(saved_prompts)

    messages.append({"role": "user", "content": up})

    print(messages)
    response = sing.generate_message_response(messages, max_tokens=rt, stream=False)
    print("Response:", response)

    save = input("Do you want to save the response? (yes/no) ").strip().lower()
    if save == 'yes':
        sing.save_response("user", up)
        sing.save_response("assistant", response)
        print("Response saved to saved_prompts.json")

if __name__ == "__main__":
    main()
