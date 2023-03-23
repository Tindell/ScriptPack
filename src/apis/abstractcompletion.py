from abc import ABC, abstractmethod


class AbstractCompletion(ABC):
    @abstractmethod
    def generate_response(self, messages, max_tokens=100, n=1, temperature=0.5, stream=None):
        pass