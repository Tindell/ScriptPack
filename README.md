# ScriptPack
## Running locally
```
> cd .../src/utils
> ./LinkScripts.sh
```
Then you can run each script by name anywhere. like `commitmeant`


https://apple.stackexchange.com/questions/399428/how-to-close-the-terminal-app-using-the-terminal-command-lineexit-in-macos-c

# Files:
## Scripts:
### [`singleshot.py`](./src/cli/singleshot.py)
This script prompts the user to enter a system prompt, a user prompt, and the maximum number of response tokens, and generates a response, printing it to the console as it is generated.
### [`cliptweak.py`](./src/cli/cliptweak.py)
This script uses the `ClipTweak` class, a subclass of `OpenAIInteraction`, to modify text copied to the clipboard. The user selects a system prompt and the maximum number of response tokens, and the GPT-3 model generates a modified response. The modified text is then copied back to the clipboard and printed to the console. The script includes two system prompts to choose from.
### [`manhunt.py`](./src/cli/manhunt.py)
This script defines a `ManSearch` class, a subclass of `OpenAIInteraction`, which can search a man page for a specified command and return information about that command. The script prompts the user to enter a command and then retrieves the corresponding man page. It then prompts the user to enter a query and calls the `generate_response` method to generate a response using the GPT-3 model. If the man page is too long, it prints an error message.
### [`mayberegex.py`](./src/cli/mayberegex.py)
This script defines a `mayberegex` class that uses the OpenAI API to generate a regular expression pattern based on a user prompt. It validates the response and tests the generated regex on sample inputs and user inputs. The script prompts the user to input their own strings and checks if they match the generated regex pattern.
### [`commitmeant.py`](./src/cli/commitmeant.py)
This script defines a `Commitmeant` class that uses GPT's API to generate a concise commit message for Git repositories. It checks if the script is being run inside a Git repository, stages changes, gets a Git diff, and commits the changes with a GPT-generated commit message. The user is prompted to accept or reject the generated commit message. The script exits if the token length of the Git diff is too large or if there are no changes detected to commit.
### [`promptprompt.py`](./src/cli/promptprompt.py)
`promptprompt` is designed to assist users in creating comprehensive prompts for ChatGPT to respond to user requests. The class ensures that prompts are clear, concise, and contain all necessary information for ChatGPT to understand the user's request and provide an appropriate response. It also takes into account potential errors or misunderstandings and provides suggestions for correcting them.

This is much better as a few-shot problem, so there are the configuration options `save_prompts` and `load_prompts` for keeping track of good responses. 

## Base files:
### [`openaiinteractions.py`](./src/openaiinteractions.py)
This script defines a class called `OpenAIInteraction` that interacts with OpenAI's GPT-3 language model to generate responses to user prompts. The class reads parameters such as the API key and model to be used from a configuration file. It provides two main methods, `generate_message_response` and `generate_response`, which take in user prompts and generate responses using the GPT-3 model. The class also includes methods to count the number of tokens used by a list of messages or a string. These methods can be used for debugging or to ensure that responses do not exceed the token limits imposed by OpenAI.
### [`openterm.py`](./src/utils/openterm.py)
This script opens a new terminal window and runs a specified command (only on macOS). It can be used to automate running these scripts outside of the terminal, for example binding cliptweak to a key binding.
