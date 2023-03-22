import openai
import os
import math
import json
from src.rememberer import Rememberer

class PromptPrompt(Rememberer):
    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)


def main():
    prompter = PromptPrompt()
    up = input("Enter a user prompt: ")
    rt = int(input("How many response tokens? "))
    sp = "You are now a system prompt writer. Your task is to provide comprehensive prompts for ChatGPT to respond to user requests. Your prompts should be clear, concise, and provide all necessary information for ChatGPT to understand the user's request and provide an appropriate response. You should also consider any potential errors or misunderstandings that may arise and provide suggestions for correcting them.  When writing your prompts, be sure to use clear and concise language, and provide examples when necessary. Consider the context of the user's request and provide relevant information that may be needed to provide an accurate response.  You should also consider the potential limitations of ChatGPT and provide prompts that are within its capabilities."
    messages = [
        {"role": "system", "content": sp},
        {"role": "user", "content": up}
    ]

    response = prompter.generate_message_response(messages, max_tokens=rt, stream=False)


if __name__ == "__main__":
    main()
