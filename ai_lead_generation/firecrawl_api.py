# import requests
# from config import FIRECRAWL_API_KEY, FIRECRAWL_BASE_URL

# def search_leads(query, max_results=10):
#     """Fetch potential leads using Firecrawl API."""
#     url = f"{FIRECRAWL_BASE_URL}search"
#     headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
#     params = {"query": query, "limit": max_results}
    
#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         return response.json().get("results", [])
#     else:
#         print(f"Error: {response.json()}")
#         return []


# import requests
# from config import FIRECRAWL_API_KEY, FIRECRAWL_BASE_URL

# def search_leads(query, max_results=10):
#     """Fetch potential leads using Firecrawl API."""
#     url = f"{FIRECRAWL_BASE_URL}search"
#     headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
#     params = {"query": query, "limit": max_results}
    
#     response = requests.get(url, headers=headers, params=params)
    
#     # Print response for debugging
#     print("🔥 Raw API Response:", response.status_code, response.text)

#     if response.status_code == 200:
#         try:
#             return response.json().get("results", [])
#         except requests.exceptions.JSONDecodeError:
#             print("❌ Error: Response is not in JSON format.")
#             return []
#     else:
#         print(f"❌ API Error: {response.status_code} - {response.text}")
#         return []


import requests
from config import FIRECRAWL_API_KEY, FIRECRAWL_BASE_URL

def search_leads(query, max_results=10):
    """Fetch potential leads using Firecrawl API."""
    url = f"{FIRECRAWL_BASE_URL}crawl"  # Change `/search` to the correct endpoint
    headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
    params = {"query": query, "limit": max_results}
    
    response = requests.get(url, headers=headers, params=params)

    # Debugging print statement
    print("🔥 Raw API Response:", response.status_code, response.text)

    if response.status_code == 200:
        try:
            return response.json().get("results", [])
        except requests.exceptions.JSONDecodeError:
            print("❌ Error: Response is not in JSON format.")
            return []
    else:
        print(f"❌ API Error: {response.status_code} - {response.text}")
        return []
