import openai
import os
import math
import sys
from src.openaiinteractions import OpenAIInteraction

class SingleShot(OpenAIInteraction):
    def __init__(self):
        super().__init__()



def main():
    sing = SingleShot()
    sp = input("Enter a system prompt: ")

    # read file from first command line argument as user prompt
    up = ""
    if len(sys.argv) > 1:
        up = open(sys.argv[1], 'r').read()
    else:
        up = input("Enter a user prompt: ")
    
    # count the tokens in the user prompt using   def num_tokens_from_string(self, string, model="gpt-3.5-turbo-0301")
    tokens = sing.num_tokens_from_string(up)
    

    rt = int(input("How many response tokens? The provided file has " + str(tokens) + " tokens."))

    print("Response:")
    sing.generate_response(sp, up, rt, stream=True)

if __name__ == "__main__":
    main()