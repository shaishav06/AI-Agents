import subprocess
import json
from config import OLLAMA_PATH, OLLAMA_URL, MODEL_NAME
from ollama_agent import process_lead_info


def generate_lead_summary(leads):
    """Process leads using Ollama AI model."""
    input_data = json.dumps({"leads": leads})
    
    command = [
        OLLAMA_PATH,
        "run",
        MODEL_NAME,
        "--prompt", f"Summarize these leads and provide key insights:\n{input_data}"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, env={"OLLAMA_URL": OLLAMA_URL})
        return result.stdout.strip()
    except Exception as e:
        print(f"Error in Ollama processing: {e}")
        return None

def process_lead_info(lead_data):
    from ollama_agent import process_lead_info
    # Process the extracted lead data
    return {"processed": True, "data": lead_data}

def use_process_lead():
    from ollama_agent import process_lead_info
    lead_data = {"name": "John Doe", "email": "john@example.com"}
    return process_lead_info(lead_data)
