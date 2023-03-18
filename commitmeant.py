import os
import subprocess
import openai

# Read the API key from the api_key file
with open("openai.key", "r") as api_key_file:
    OPENAI_API_KEY = api_key_file.read().strip()

# Set the API key for the openai library
openai.api_key = OPENAI_API_KEY

# Ensure the working directory is a git repository
try:
    subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True)
except subprocess.CalledProcessError:
    print("This script must be run inside a git repository.")
    exit(1)

# Stage all current changes
subprocess.run(["git", "add", "."])

# Check for uncommitted changes
if not subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"]).returncode:
    print("No changes detected. Exiting.")
    exit(0)

# Get the git diff
git_diff = subprocess.run(["git", "diff",  "--cached", "--no-color"], capture_output=True, text=True).stdout

print("Raw diff: ", git_diff)

# Generate the commit message using the OpenAI Chat API
messages = [
    {"role": "system", "content": "Generate a commit message based on the following git diff:"},
    {"role": "user", "content": git_diff},
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=50,
    n=1,
    temperature=0.5,
)

# Print the raw API response
print("Raw API response:", response)

commit_message = response.choices[0].message["content"].strip()

# Commit the changes with the generated message
subprocess.run(["git", "commit", "-m", commit_message])

print(f"Committed changes with message: {commit_message}")