import google.generativeai as genai
from utils.config import GEMINI_API_KEY

class GeminiAgent:
    def __init__(self):
        """Initialize Gemini API Client."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")

    def schedule_appointment(self, details):
        """Generate appointment confirmation messages."""
        response = self.model.generate_content(f"Schedule an appointment with details: {details}")
        return response.text
