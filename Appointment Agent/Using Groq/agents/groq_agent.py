from groq import Client
from utils.config import GROQ_API_KEY

class GroqAgent:
    def __init__(self):
        """Initialize Groq API Client."""
        self.client = Client(api_key=GROQ_API_KEY)

    def answer_query(self, query):
        """Generate responses for appointment-related queries."""
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",  # Use an appropriate model
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
