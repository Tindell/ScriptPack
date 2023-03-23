from src.apis.abstractcompletion import AbstractCompletion
import openai

class OpenAICompletion(AbstractCompletion):
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def generate_response(self, messages, max_tokens=100, n=1, temperature=0.5, stream=None):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            n=n,
            temperature=temperature,
            stream=stream,
        )
        return response