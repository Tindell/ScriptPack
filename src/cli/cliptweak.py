import pyperclip
import math
from src.rememberer import Rememberer

system_prompts = {
    "1": {
        "description": "Simplify copied python code",
        "prompt": "Simplify the following python code.  Return only the new python code, with no explaination.",
    },
    "2": {
        "description": "Summarize copied text",
        "prompt": "Generate a summary for the following text:",
    },
    "3": {
        "description": "Write a comment describing CPP code",
        "prompt": "Write a c++ comment with regular line breaks describing the following C++ code:",
    },
}

class ClipTweak(Rememberer):
    def __init__(self):
        super().__init__()

    def process_clipboard_content(self, clipboard_content):
        print("Processing text")
        system_prompt_id, system_prompt = self.select_a_prompt()
        leng = self.select_a_length(len(clipboard_content))

        if leng > 2000:
            leng = 2000

        assistant_reply = self.generate_response(system_prompt, clipboard_content, leng, file_name=f"{self.__class__.__name__}-{system_prompt_id}")
        return assistant_reply.strip()

    def select_a_prompt(self):
        print("Please choose a system prompt:")
        for prompt_id, prompt_data in system_prompts.items():
            print(f"{prompt_id}: {prompt_data['description']}")

        choice = input("Enter the prompt number: ")
        return choice, system_prompts[choice]['prompt']

    def select_a_length(self, num_letters):
        print(f"How many tokens should I reply with? You sent me roughly {math.ceil(num_letters / 4)} tokens")
        return int(input())

def main():
    clipboard_text = pyperclip.paste()
    ct = ClipTweak()
    modified_text = ct.process_clipboard_content(clipboard_text)
    pyperclip.copy(modified_text)
    print("Modified text:", modified_text)

if __name__ == "__main__":
    main()
