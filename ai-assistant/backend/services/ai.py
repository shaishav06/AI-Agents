import openai

GROQ_API_KEY = "your_groq_api_key"
GEMINI_API_KEY = "your_gemini_api_key"

def generate_email(prompt):
    """Generate email content using Gemini AI"""
    response = openai.ChatCompletion.create(
        model="gemini",
        messages=[{"role": "user", "content": prompt}],
        api_key=GEMINI_API_KEY
    )
    return response["choices"][0]["message"]["content"]

def generate_leads(industry, count=5):
    """Generate business leads using Groq AI"""
    response = openai.ChatCompletion.create(
        model="groq",
        messages=[{"role": "user", "content": f"Find {count} leads in {industry}"}],
        api_key=GROQ_API_KEY
    )
    return response["choices"][0]["message"]["content"]
