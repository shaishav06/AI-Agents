import os
from groq import Client
from utils.config import GROQ_API_KEY

class GroqModel:
    def __init__(self):
        self.client = Client(api_key=GROQ_API_KEY)

    def answer(self, question):
        """Answer academic queries using Groq API."""
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",  # Adjust model as needed
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
