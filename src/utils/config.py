import argparse
import configparser
import os
import sys

class Config:
    def __init__(self, config_file='config.ini'):
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', dest='model',
                            help='Specify the OpenAI model')
        parser.add_argument('--printResponse', dest='printResponse', type=bool,
                            help='Specify whether to print OpenAI response')
        parser.add_argument('--operation', dest='operation',
                            help='Specify the OpenAI operation')
        parser.add_argument('--api_key', dest='api_key',
                            help='Specify the OpenAI API key')
        parser.add_argument('--saved_prompts_location', dest='saved_prompts_location',
                            help='Specify the directory to save/load prompts from')
        parser.add_argument('--load_prompts', dest='load_prompts', type=bool,
                            help='Specify whether to load prompts from file')
        parser.add_argument('--save_prompts', dest='save_prompts', type=bool,
                            help='Specify whether to save prompts to file')
        parser.add_argument('--stream', '-s', dest='stream', type=bool, default=False,
                            help='Specify whether to stream the response from OpenAI')
        parser.add_argument('-f', '--file', dest='system_prompt_file',
                            help='Specify the system prompt file; not always used')
        parser.add_argument('-t', '--max_tokens', dest='max_tokens', type=int,
                            help='Specify the number of tokens for OpenAI response')

        self.args = parser.parse_args()

        # This is a hack to get the config file to load properly when run with runInCD 
        config_file = os.path.join(sys.path[0], config_file)
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        if self.args.model:
            self.config.set('OPENAI', 'model', self.args.model)
        if self.args.printResponse:
            self.config.set('OPENAI', 'printResponse', str(self.args.printResponse))
        if self.args.operation:
            self.config.set('OPENAI', 'operation', self.args.operation)
        if self.args.api_key:
            os.environ['OPENAI_API_KEY'] = self.args.api_key
        if self.args.saved_prompts_location:
            self.config.set('OPENAI', 'saved_prompts_location', self.args.saved_prompts_location)
        if self.args.load_prompts:
            self.config.set('OPENAI', 'load_prompts', str(self.args.load_prompts))
        if self.args.save_prompts:
            self.config.set('OPENAI', 'save_prompts', str(self.args.save_prompts))
        if self.args.stream:
            self.config.set('OPENAI', 'stream', str(self.args.stream))
        if self.args.max_tokens:
            self.config.set('OPENAI', 'max_tokens', str(self.args.max_tokens))

    def get_model(self):
        return self.config.get('OPENAI', 'model', fallback='gpt-3.5-turbo')

    def get_print_response(self):
        return self.config.getboolean('OPENAI', 'printResponse', fallback=True)

    def get_operation(self):
        return self.config.get('OPENAI', 'operation', fallback='generate_response')

    def get_api_key(self):
        return os.getenv('OPENAI_API_KEY')

    def get_saved_prompts_location(self):
        return self.config.get('OPENAI', 'saved_prompts_location', fallback='saved_prompts')

    def get_load_prompts(self):
        return self.config.getboolean('OPENAI', 'load_prompts', fallback=True)

    def get_save_prompts(self):
        return self.config.getboolean('OPENAI', 'save_prompts', fallback=True)

    def get_stream(self):
        return self.config.getboolean('OPENAI', 'stream', fallback=False)
    
    def get_system_prompt_file(self):
        return self.args.system_prompt_file

    def get_max_tokens(self):
        return self.config.getint('OPENAI', 'max_tokens', fallback=100)