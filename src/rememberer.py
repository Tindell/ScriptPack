import os
import json
import configparser
import sys
from src.openaiinteractions import OpenAIInteraction


class Rememberer(OpenAIInteraction):
    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)
        self.saved_prompts_location = self.config.get('OPENAI', 'saved_prompts_location', fallback='saved_prompts')
        self.load_prompts = self.config.getboolean('OPENAI', 'load_prompts', fallback=True)
        self.save_prompts = self.config.getboolean('OPENAI', 'save_prompts', fallback=True)

    def save_prompt(self, prompt, response, saved_prompts_filename):
        saved_prompts = self.load_saved_prompts(saved_prompts_filename)
        filepath = os.path.join(self.saved_prompts_location, saved_prompts_filename)
        print(f"\n\nResponse: {response}")
        save = input("Do you want to save the response? (yes/no) ").strip().lower()
        if save == 'yes':
            os.makedirs(self.saved_prompts_location, exist_ok=True)

            saved_prompts.append(prompt)
            saved_prompts.append({"role": "assistant", "content": response})

            with open(filepath, 'w') as file:
                json.dump(saved_prompts, file, indent=4)

            print(f"Response saved to {filepath}")

    def load_saved_prompts(self, saved_prompts_filename):
        filepath = os.path.join(self.saved_prompts_location, saved_prompts_filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                saved_prompts = json.load(file)
            return saved_prompts
        else:
            return []
        
    
    def load_prompts_into_messages(self, messages, saved_prompts_filename):
        new_messages = []
        # add the system prompt from the original message into new_messages
        new_messages.append(messages[0])
        # add all saved prompts into new_messages
        new_messages.extend(self.load_saved_prompts(saved_prompts_filename))
        # add all but the first message in messages into new_messages
        new_messages.extend(messages[1:])

        return new_messages
    
    def generate_message_response(self, message, max_tokens=100, temperature=0.5, stream=False, file_name=None):
        if not file_name:
            file_name = self.__class__.__name__
        saved_prompts_filename = f"saved_prompts.{file_name}.json"

        if self.load_prompts:
            modified_message = self.load_prompts_into_messages(message, saved_prompts_filename)
        else:
            modified_message = message

        if self.printResponse:
            print("Modified message: ", modified_message)

        response = super().generate_message_response(modified_message, max_tokens, temperature, stream)

        if self.save_prompts and not stream:
            self.save_prompt(modified_message[-1], response, saved_prompts_filename)

        return response
    
    def generate_response(self, system_prompt, user_content, max_tokens=100, temperature=0.5, stream=False, file_name=None):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        return self.generate_message_response(messages, max_tokens, temperature, stream, file_name)
