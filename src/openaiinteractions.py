import os
import openai
import configparser
import sys
import tiktoken
import json

class OpenAIInteraction:
    def __init__(self, config_file='config.ini'):
        print(config_file)

        # This is a hack to get the config file to load properly when run with runInCD 
        config_file = os.path.join(sys.path[0], config_file)

        config = configparser.ConfigParser()
        config.read(config_file)
        print(config.sections())

        self.model = config.get('OPENAI', 'model', fallback='gpt-3.5-turbo')
        self.printResponse = config.get('OPENAI', 'printResponse', fallback=True)
        self.operation = config.get('OPENAI', 'operation', fallback='generate_response')
        self.saved_prompts_location = config.get('OPENAI', 'saved_prompts_location', fallback='saved_prompts')
        self.saved_prompts_filename = f"saved_prompts.{self.__class__.__name__}.json"
        self.load_prompts = config.get('OPENAI', 'load_prompts', fallback=True)
        self.save_prompts = config.get('OPENAI', 'save_prompts', fallback=True)

        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def save_prompt(self, prompt, response):
        saved_prompts = self.load_saved_prompts()
        filepath = os.path.join(self.saved_prompts_location, self.saved_prompts_filename)

        save = input("Do you want to save the response? (yes/no) ").strip().lower()
        if save == 'yes':
            os.makedirs(self.saved_prompts_location, exist_ok=True)

            saved_prompts.append(prompt)
            saved_prompts.append({"role": "assistant", "content": response})

            with open(filepath, 'w') as file:
                json.dump(saved_prompts, file, indent=4)

            print(f"Response saved to {filepath}")

    def load_saved_prompts(self):
        filepath = os.path.join(self.saved_prompts_location, self.saved_prompts_filename)
        print(self.saved_prompts_location)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                saved_prompts = json.load(file)
            return saved_prompts
        else:
            return []

    def load_prompts_into_messages(self, messages):
        new_messages = []
        # add the system prompt from the original message into new_messages
        new_messages.append(messages[0])
        # add all saved prompts into new_messages
        new_messages.extend(self.load_saved_prompts())
        # add all but the first message in messages into new_messages
        new_messages.extend(messages[1:])

        return new_messages

    def generate_message_response(self, message, max_tokens=100, temperature=0.5, stream=False):
        modified_message = self.load_prompts_into_messages(message)
        if self.printResponse:
            print("Modified message: ", modified_message)
            
        
        if self.operation == 'generate_response':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=modified_message,
                max_tokens=max_tokens,
                n=1,
                temperature=temperature,
                stream=stream,
            )

            # TODO: maybe just return the stream? streaming should probably be it's own method
            if(stream):
                ret = ""
                # receive a stream of text from the model
                for chunk in response:
                    if "delta" in chunk.choices[0] and "content" in chunk["choices"][0]["delta"]:
                            ret += chunk["choices"][0]["delta"]["content"]
                            print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
                print()
                # when streaming, don't do any of the extra processing, like saving the response
                return ret

            if self.printResponse:
                print("Complete response: ", response)

            if(self.save_prompts):
                self.save_prompt(modified_message[-1], response.choices[0].message.content.strip())

            return response.choices[0].message.content.strip()

        # This option exists for debugging and creating.
        elif self.operation == 'count_tokens':
            num_tokens = self.num_tokens_from_messages(modified_message)
            return num_tokens

        else:
            raise ValueError(f"Invalid operation: {self.operation}. Supported operations are 'generate_response' and 'count_tokens'.")



    def generate_response(self, system_prompt, user_content, max_tokens=100, temperature=0.5, stream=False):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        return self.generate_message_response(messages, max_tokens, temperature, stream)

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

    def num_tokens_from_string(self, string, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a string."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":
            num_tokens = 4  # start token, role/name, newline, content
            num_tokens += len(encoding.encode(string))
            num_tokens += 2  # end token
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_string() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")