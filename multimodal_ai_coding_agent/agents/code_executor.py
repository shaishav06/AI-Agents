from e2b import ExecutionClient
from utils.config import E2B_API_KEY

class CodeExecutor:
    def __init__(self):
        self.client = e2b.ExecutionClient(api_key=E2B_API_KEY)

    def run_code(self, code: str, language="python"):
        execution = self.client.execute(language=language, code=code)
        return execution.get_output()

# Example usage
if __name__ == "__main__":
    executor = CodeExecutor()
    output = executor.run_code("print('Hello, AI!')")
    print(output)
