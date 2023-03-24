import os
import sys

def main(name):
    if not name:
        sys.exit(0)
    # Start a new terminal window and run the provided script.  It doesn't work with args yet.
    if sys.platform == "darwin":  # macOS
        os.system(f"osascript -e 'tell application \"Terminal\" to do script \""+name+"; exit\" activate'")
    else:
        print("This script currently supports macOS only.")

if __name__ == "__main__":
    main(sys.argv[1])