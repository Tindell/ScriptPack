import sys
import json
import re
import openai
import os
from src.rememberer import Rememberer

system_messages = [
    {
        "role": "system",
        "content": "Your job is to provide me a regex string that can be parsed in python based off of the query I ask in English. Provide your answer as a JSON document containing the explanation, examples that will match, and the regex. Provide nothing but the JSON. Make sure it is valid JSON."
    },
    {
        "role": "user",
        "content": "Find all the lines that contain only lower case letters and spaces"
    },
    {
        "role": "assistant",
        "content": '{"explanation": "This regex will match any line that contains only lower case letters and spaces. The \'^\' and \'$\' anchors ensure that the regex matches the entire line. The \'+\' quantifier after the character set \'[a-z ]\' matches one or more occurrences of lower case letters or spaces. The \'^$\' alternative matches empty lines.", "examples": ["hello world","this is a line with spaces","justlowercaseletters"," a line starting with a space and lowercase letters"],  "regex": "^[a-z ]+$|^$"}'
    },
    {
        "role": "user",
        "content": "Find the words separated by a '-'. Example lines that will match include  'Auto-tagging is helpful' or 'You should focus on note-taking'"
    },
    {
        "role": "assistant",
        "content": '{"explanation": "This regex will match any line that contains words separated by a \'-\' character. The character set \'\\\\w\' matches any word character (alphanumeric or underscore), the \'+\' quantifier matches one or more occurrences of word characters, and the \'-\' character is matched. The whole pattern is repeated one or more times with the \'\\\\s+\' to match one or more non-word characters between each group of words.",  "examples": ["Auto-tagging is helpful","You should focus on note-taking","This-line-has-four-words"],  "regex": "\\\\w+(?:-\\\\w+)+"}'
    }
]


class mayberegex(Rememberer):
    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)

    def fetch_json_data(self, prompt):
        system_messages.append({"role": "user", "content": prompt})
        return self.generate_message_response(system_messages, 150)

    def is_valid_json(self, json_str):
        try:
            data = json.loads(json_str)
        except ValueError as e:
            print(f"Invalid JSON: {e}")
            return False

        if not isinstance(data, dict):
            print("Malformatted response form OPENAI. JSON data must be a dictionary")
            return False

        if "examples" not in data or "regex" not in data or "explanation" not in data:
            print("Malformatted response form OPENAI. JSON data must contain 'examples', 'explanation' and 'regex' keys")
            return False

        if not (isinstance(data["examples"], list) and isinstance(data["regex"], str) and isinstance(data["explanation"], str)):
            print("Malformatted response form OPENAI.  'examples' and 'explanation' must be a list and 'regex' must be a string")
            return False

        return True

    def test_regex(self, json_data):
        if not self.is_valid_json(json_data):
            print("Invalid JSON data")
            return
        
        data = json.loads(json_data)
        examples = data["examples"]
        regex_pattern = data["regex"]
        print("\nPattern: ", regex_pattern, "\n\n")
        print("Reasoning: ", data["explanation"])
        print("Testing the Regex Pattern: ", regex_pattern, " with generated input\n")
        
        for example in examples:
            example = example.strip()
            match = re.search(regex_pattern, example)
            if match:
                print(f"{example}:\nMatch")
            else:
                print(f"{example}:\nNo Match")

        self.user_input_regex_test(regex_pattern)

    def user_input_regex_test(self, regex_pattern):
        print(f"\nTesting user input against regex pattern: {regex_pattern}")
        print("Enter 'q' or 'Q' to quit.")

        while True:
            user_input = input("Enter your input: ")

            if user_input.lower() == 'q':
                break

            match = re.search(regex_pattern, user_input)
            if match:
                print("Match")
            else:
                print("No Match")

def main():
    prompt = input("Please enter a prompt: ")

    if not prompt:
        print("nothing")
        sys.exit(1)

    mr = mayberegex()

    json_data = mr.fetch_json_data(prompt)
    mr.test_regex(json_data)

if __name__ == "__main__":
    main()