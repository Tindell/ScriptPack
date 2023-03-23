import os
import subprocess
from src.openaiinteractions import OpenAIInteraction

# This one isn't very useful, because man pages are usually longer than 4k tokens.

system_prompt = "Your job is to find information in a provided man page.  If the information requested isn't in the page, your job is to say 'I can't find anything about that'."

class ManSearch(OpenAIInteraction):
    def __init__(self):
        super().__init__()

    def get_man_page(self, command):
        try:
            man_page = subprocess.check_output(["man", command])
            return man_page.decode("utf-8")
        except subprocess.CalledProcessError:
            return f"No manual entry for {command}\n"

def main():
    mans = ManSearch()
    command = input("Enter a command: ")
    man_page = mans.get_man_page(command)

    if(mans.num_tokens_from_string(man_page) >= 3500):
        print("That man page is too long to fit in one request.")
        return
    
    prompt = input("Enter a query: ") 

    # Send the command name and man page to generate_response
    mans.generate_response(system_prompt, f"{prompt}\n\n'''\n{man_page}\n'''", 100, stream=True)

if __name__ == "__main__":
    main()