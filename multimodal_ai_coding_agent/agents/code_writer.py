import ollama

class CodeWriter:
    def __init__(self):
        self.model = "o3-mini"

    def generate_code(self, prompt: str):
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

# Example usage
if __name__ == "__main__":
    writer = CodeWriter()
    code = writer.generate_code("Write a Python function to calculate factorial.")
    print(code)
