import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """Fetches and extracts text content from a webpage."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return " ".join([p.text for p in soup.find_all("p")])
        else:
            return f"Error: Unable to fetch the page (Status Code: {response.status_code})"
    except Exception as e:
        return f"Error: {e}"
