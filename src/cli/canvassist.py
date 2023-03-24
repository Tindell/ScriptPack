from src.openaiinteractions import OpenAIInteraction

class CanvAssist(OpenAIInteraction):
    def __init__(self):
        super().__init__()

    def run(self):
        sp = """
        You are a canvas artist.  You generate drawings for HTML canvas elements.  You are given a description of the drawing you should create.  You are also given a canvas element to draw on.  The canvas is 400px wide and 300px tall.  Base your code on the following function:
        function mountain(canvas, title) {
            
            const ctx = canvas.getContext("2d");
            ... 
        }
        """
        print("Welcome to CanvAI! Please provide a description of the drawing you would like to create.")
        up = input("Description: ")

        max_tokens = self.config.get_max_tokens()

        print("Generating drawing...")
        self.generate_response(sp, up, max_tokens=3000, stream=True)

def main():
    CanvAssist().run()

if __name__ == "__main__":
    main()
