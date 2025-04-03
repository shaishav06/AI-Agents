import os

# Ollama (o3-mini) settings
OLLAMA_MODEL = "o3-mini"

# Google Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "Your_Gemini_API_KEY")

# E2B (Execution Environment)
E2B_API_KEY = os.getenv("E2B_API_KEY", "Your_E2B_API_KEY")
