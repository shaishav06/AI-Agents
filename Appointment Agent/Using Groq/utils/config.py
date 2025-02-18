import os
from dotenv import load_dotenv

# Get absolute path of the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Debug: Check if .env file exists
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env file not found at: {ENV_PATH}")

# Load .env file
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Fetch API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Debug: Print loaded keys (Remove this after testing)
print(f"Loaded API Keys: GROQ={GROQ_API_KEY}, GEMINI={GEMINI_API_KEY}")

# Validate API keys
if not GROQ_API_KEY or not GEMINI_API_KEY:
    raise ValueError(f"Missing API keys! Check your .env file at: {ENV_PATH}")
