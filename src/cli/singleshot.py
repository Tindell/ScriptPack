import openai
import os
import math
from src.openaiinteractions import OpenAIInteraction

class SingleShot(OpenAIInteraction):
    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)



def main():
    sing = SingleShot()
    sp = input("Enter a system prompt: ")
    up = input("Enter a user prompt: ")
    rt = int(input("How many response tokens? "))

    print("Response:")
    sing.generate_response(sp, up, rt, stream=True)

if __name__ == "__main__":
    main()