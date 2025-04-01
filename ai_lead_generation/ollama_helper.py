import os
import requests
import json

class OllamaClient:
    """
    A helper class to interact with the Ollama API if the native Python client
    doesn't support certain functionalities or has version compatibility issues.
    """
    
    def __init__(self, base_url=None):
        """
        Initialize the Ollama client with the base URL.
        
        Args:
            base_url (str): The base URL for the Ollama API. If None, will use the OLLAMA_HOST 
                           environment variable or default to http://localhost:11434
        """
        if base_url is None:
            base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        
        # Ensure base_url has a proper http prefix
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"
            
        # Remove trailing slash if present
        if base_url.endswith("/"):
            base_url = base_url[:-1]
            
        self.base_url = base_url
    
    def list_models(self):
        """List all available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to list models: {response.status_code} - {response.text}"}
        except Exception as e:
            return {"error": f"Exception when listing models: {str(e)}"}
    
    def generate_completion(self, model, prompt, options=None):
        """
        Generate a completion from the model.
        
        Args:
            model (str): The name of the model to use
            prompt (str): The prompt to generate a completion for
            options (dict): Additional options for generation
            
        Returns:
            dict: The response from the API
        """
        endpoint = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        if options:
            payload.update(options)
            
        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                # The response is a series of JSON objects, one per line
                result = ""
                for line in response.text.strip().split("\n"):
                    line_data = json.loads(line)
                    if "response" in line_data:
                        result += line_data["response"]
                return {"text": result}
            else:
                return {"error": f"Failed to generate completion: {response.status_code} - {response.text}"}
        except Exception as e:
            return {"error": f"Exception when generating completion: {str(e)}"}
    
    def chat(self, model, messages, options=None):
        """
        Generate a chat completion from the model.
        
        Args:
            model (str): The name of the model to use
            messages (list): A list of message dictionaries with 'role' and 'content'
            options (dict): Additional options for generation
            
        Returns:
            dict: The response from the API with the assistant's message
        """
        endpoint = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if options:
            payload.update(options)
            
        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                # The response is a series of JSON objects, one per line
                full_response = ""
                for line in response.text.strip().split("\n"):
                    line_data = json.loads(line)
                    if "message" in line_data:
                        # This is the final message object
                        return {
                            "message": line_data["message"]
                        }
                    elif "content" in line_data:
                        # This is a streaming chunk
                        full_response += line_data.get("content", "")
                
                # If we didn't get a message object, construct one from the streamed content
                if full_response:
                    return {
                        "message": {
                            "role": "assistant",
                            "content": full_response
                        }
                    }
                return {"error": "No response content received"}
            else:
                return {"error": f"Failed to generate chat completion: {response.status_code} - {response.text}"}
        except Exception as e:
            return {"error": f"Exception when generating chat completion: {str(e)}"}