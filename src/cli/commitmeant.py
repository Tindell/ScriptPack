import os
import subprocess
from src.openaiinteractions import OpenAIInteraction

class GitCommitHelper(OpenAIInteraction):
    def __init__(self):
        super().__init__()

    def check_git_repository(self):
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("This script must be run inside a git repository.")
            exit(1)

    def stage_changes(self):
        subprocess.run(["git", "add", "."])

    def no_changes_detected(self):
        return not subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"]).returncode

    def get_git_diff(self):
        git_diff = subprocess.run(["git", "diff", "--cached", "--no-color"], capture_output=True, text=True).stdout
        messages = [
            {"role": "system", "content": "Generate a short and concise commit message based on the following git diff:"},
            {"role": "user", "content": git_diff},
        ]
        token_length = self.num_tokens_from_messages(messages)

        if token_length > 4097:
            print("Token length of the git diff is too large (> 4097). Cancelling commit.")
            exit(1)

        return git_diff

    def commit_changes(self, commit_message):
        subprocess.run(["git", "commit", "-m", commit_message])
        print(f"Committed changes with message: {commit_message}")

def main():
    git_helper = GitCommitHelper()

    git_helper.check_git_repository()
    git_helper.stage_changes()

    if git_helper.no_changes_detected():
        print("No changes detected. Exiting.")
        exit(0)

    git_diff = git_helper.get_git_diff()
    print("Raw diff: ", git_diff)

    commit_message = ""
    user_accepts = False

    while not user_accepts:
        commit_message = git_helper.generate_response(
            system_prompt="Generate a short and concise commit message based on the following git diff:",
            user_content=git_diff,
        )

        print(f"Suggested commit message: {commit_message}")
        user_input = input("Is this commit message acceptable? (yes/no): ").lower()

        if user_input in ["yes", "y"]:
            user_accepts = True

    git_helper.commit_changes(commit_message)

if __name__ == "__main__":
    main()
