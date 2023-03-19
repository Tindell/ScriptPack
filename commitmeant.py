import os
import subprocess
import openai

def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    openai.api_key = OPENAI_API_KEY

    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("This script must be run inside a git repository.")
        exit(1)

    subprocess.run(["git", "add", "."])

    if not subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"]).returncode:
        print("No changes detected. Exiting.")
        exit(0)

    git_diff = subprocess.run(["git", "diff",  "--cached", "--no-color"], capture_output=True, text=True).stdout

    print("Raw diff: ", git_diff)

    commit_message = ""
    user_accepts = False

    while not user_accepts:
        messages = [
            {"role": "system", "content": "Generate a short and concise commit message based on the following git diff:"},
            {"role": "user", "content": git_diff},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            n=1,
            temperature=0.5,
        )

        print("Raw API response:", response)

        commit_message = response.choices[0].message["content"].strip()

        print(f"Suggested commit message: {commit_message}")
        user_input = input("Is this commit message acceptable? (yes/no): ").lower()

        if user_input in ["yes", "y"]:
            user_accepts = True

    subprocess.run(["git", "commit", "-m", commit_message])

    print(f"Committed changes with message: {commit_message}")

if __name__ == "__main__":
    main()