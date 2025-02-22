import google.generativeai as genai
from utils.config import GEMINI_API_KEY

class GeminiModel:
    def __init__(self):
        """Configure Gemini API key."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")  # Use the correct model

    def generate_text(self, query):
        """Generate study materials based on query."""
        response = self.model.generate_content(query)
        return response.text  # Extract text from response
