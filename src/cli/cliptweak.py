import pyperclip
import openai
import os
import math
from src.openaiinteractions import OpenAIInteraction

system_prompts = {
    "Simplify copied python code": "Simplify the following python code.  Return only the new python code, with no explaination.",
    "Summerize copied text ": "Generate a summary for the following text:",
    "Write a comment describing CPP code": "Write a c++ comment with regular line breaks describing the following C++ code:",
}


class ClipTweak(OpenAIInteraction):
    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)


# Function to interact with OpenAI API
    def process_clipboard_content(self, clipboard_content):
        print("Processing text")
        system_prompt = self.select_a_prompt()
        leng = self.select_a_length(len(clipboard_content))
    
        if(leng > 2000):
            leng = 2000

        # Get the assistant's reply from the response
        assistant_reply = self.generate_response(system_prompt, clipboard_content, leng)

        return assistant_reply.strip()

    def select_a_prompt(self):    
        print("Please choose a system prompt:")
        for index, prompt_name in enumerate(system_prompts.keys(), start=1):
            print(f"{index}: {prompt_name}")
        choice = int(input("Enter the prompt number: "))
        return list(system_prompts.values())[choice - 1]

    def select_a_length(self, num_letters):
        # Print the list of system prompt names for the user to choose from
        print(f"How any tokens should I reply with? You sent me roughly {math.ceil(num_letters/4)} tokens")
        return int(input())

def main():
    clipboard_text = pyperclip.paste()
    ct = ClipTweak()
    modified_text = ct.process_clipboard_content(clipboard_text)
    pyperclip.copy(modified_text)
    print("Modified text:", modified_text)

if __name__ == "__main__":
    main()