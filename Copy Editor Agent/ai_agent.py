import os
from dotenv import load_dotenv
import google.generativeai as genai
import groq

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

# Initialize Groq AI
groq_client = groq.Client(api_key=GROQ_API_KEY)

def get_gemini_feedback(text):
    """Analyzes and improves webpage text using Gemini AI."""
    prompt = f"Review the following webpage content and provide clarity and effectiveness improvement tips:\n\n{text}"
    response = gemini_model.generate_content(prompt)
    return response.text if response else "No response generated."

def get_groq_feedback(text):
    """Analyzes and improves webpage text using Groq AI."""
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": f"Review this webpage content and provide improvement tips:\n\n{text}"}],
    )
    return response.choices[0].message.content if response else "No response generated."
