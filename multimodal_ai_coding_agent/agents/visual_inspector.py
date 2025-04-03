import google.generativeai as genai
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class VisualInspector:
    def analyze_image(self, image_path: str):
        model = genai.GenerativeModel('gemini-pro-vision')
        with open(image_path, "rb") as img_file:
            response = model.generate_content([img_file.read()])
        return response.text

# Example usage
if __name__ == "__main__":
    inspector = VisualInspector()
    analysis = inspector.analyze_image("example_code_screenshot.png")
    print(analysis)
