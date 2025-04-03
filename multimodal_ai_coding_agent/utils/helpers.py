import jwt
import os
import logging
from utils.config import JWT_SECRET, JWT_ALGORITHM

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_jwt(payload):
    """Generate JWT token."""
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token):
    """Decode JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def save_uploaded_file(file, filename):
    """Save uploaded file to temp directory."""
    file_path = os.path.join("temp", filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.read())
    return file_path

def validate_code_execution_output(output):
    """Validate code execution output for errors."""
    if "error" in output.lower():
        logging.error(f"Execution Error: {output}")
    return output
