import os
import openai
import configparser
import sys
import tiktoken
import json

class OpenAIInteraction:
    def __init__(self, config_file='config.ini'):
        # This is a hack to get the config file to load properly when run with runInCD 
        config_file = os.path.join(sys.path[0], config_file)
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.model = self.config.get('OPENAI', 'model', fallback='gpt-3.5-turbo')
        self.printResponse = self.config.getboolean('OPENAI', 'printResponse', fallback=True)
        self.operation = self.config.get('OPENAI', 'operation', fallback='generate_response')

        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

        # TODO override config settings with command line arguments

    def generate_message_response(self, message, max_tokens=100, temperature=0.5, stream=False):

        if self.printResponse:
            print("Modified message: ", message)
            
        
        if self.operation == 'generate_response':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=message,
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

            return response.choices[0].message.content.strip()

        # This option exists for debugging and creating.
        elif self.operation == 'count_tokens':
            num_tokens = self.num_tokens_from_messages(message)
            return num_tokens

        else:
            raise ValueError(f"Invalid operation: {self.operation}. Supported operations are 'generate_response' and 'count_tokens'.")

    def generate_response(self, system_prompt, user_content, max_tokens=100, temperature=0.5, stream=False):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        return self.generate_message_response(messages, max_tokens, temperature, stream)

    # TODO these are AI generated an not tested
    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":
            num_tokens = sum([4 + len(encoding.encode(value)) - 1 if key == "name" else 4 + len(encoding.encode(value)) for message in messages for key, value in message.items()])
            num_tokens += 2 * len(messages)
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

    def num_tokens_from_string(self, string, model="gpt-3.5-turbo-0301"):
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":
            return 4 + len(encoding.encode(string)) + 2
        else:
            raise NotImplementedError(f"""num_tokens_from_string() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
