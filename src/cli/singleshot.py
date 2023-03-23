import openai
import os
import math
import sys
from src.openaiinteractions import OpenAIInteraction

class SingleShot(OpenAIInteraction):
    def __init__(self):
        super().__init__()

    def run(self):
        sp = ""

        spf = self.config.get_system_prompt_file()
        print("spf: " + str(spf))
        if spf:
            sp = open(spf, 'r').read()
        else:
            sp = input("Enter a system prompt: ")  

        if not sys.stdin.isatty():
            up = sys.stdin.read()
        else:
            up = input("Enter a user prompt: ")

        max_tokens = self.config.get_max_tokens()
        if not max_tokens:
            tokens = self.num_tokens_from_string(up)
            max_tokens = int(input("How many response tokens? The provided file has " + str(tokens) + " tokens."))
 
        print("Response:")
        self.generate_response(sp, up, max_tokens=max_tokens, stream=True)

def main():
    SingleShot().run()

if __name__ == "__main__":
    main()