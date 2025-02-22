import os
from models.gemini_model import GeminiModel
from models.groq_model import GroqModel

class StudentAssistantAgent:
    def __init__(self):
        self.gemini_model = GeminiModel()
        self.groq_model = GroqModel()

    def retrieve_study_materials(self, query):
        """Retrieve relevant study materials using Gemini API."""
        return self.gemini_model.generate_text(query)

    def answer_query(self, question):
        """Answer academic queries using Groq API."""
        return self.groq_model.answer(question)

    def generate_study_plan(self, topic):
        """Generate a structured study plan."""
        return f"Here's a study plan for {topic}:\n1. Introduction\n2. Key Concepts\n3. Example Problems\n4. Advanced Topics\n5. Practice Exercises"
