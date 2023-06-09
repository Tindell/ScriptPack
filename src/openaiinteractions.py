import tiktoken
from src.utils.config import Config
from src.apis.abstractcompletion import AbstractCompletion
from src.apis.openaicompletion import OpenAICompletion

class OpenAIInteraction:
    def __init__(self):

        # these should be injected but I don't  want to change every child class's constructor
        config = Config()
        self.api : AbstractCompletion = OpenAICompletion(config.get_api_key(), config.get_model())
        
        self.config = config
        self.model = config.get_model()
        self.printResponse = config.get_print_response()
        self.operation = config.get_operation()
        self.api_key = config.get_api_key()
        self.stream = config.get_stream()

    def generate_message_response(self, message, max_tokens=100, temperature=0.5, stream=None):
        if(stream is None):
            stream = self.stream

        if self.printResponse:
            print("Modified message: ", message)
        
        if self.operation == 'generate_response':
            response = self.api.generate_response(
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

    def generate_response(self, system_prompt, user_content, max_tokens=100, temperature=0.5, stream=None):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        return self.generate_message_response(messages, max_tokens, temperature, stream)

    # TODO I never tested these
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
