import os
import openai
import configparser
import tiktoken
import sseclient

class OpenAIInteraction:
    def __init__(self, config_file='config.ini'):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.model = config.get('OPENAI', 'model', fallback='gpt-3.5-turbo')
        self.printResponse = config.get('OPENAI', 'printResponse', fallback=True)
        self.operation = config.get('OPENAI', 'operation', fallback='generate_response')
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key


    def generate_response(self, system_prompt, user_content, max_tokens=100, temperature=0.5, stream=False):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]

        if self.operation == 'generate_response':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
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
                    if "delta" in chunk.choices[0]:
                        if "content" in chunk["choices"][0]["delta"]:
                            ret += chunk["choices"][0]["delta"]["content"]
                            print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
                print()
                return ret

            if self.printResponse:
                print("Complete response: ", response)

            return response.choices[0].message.content.strip()

        elif self.operation == 'count_tokens':
            num_tokens = self.num_tokens_from_messages(messages)
            return num_tokens

        else:
            raise ValueError(f"Invalid operation: {self.operation}. Supported operations are 'generate_response' and 'count_tokens'.")

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
