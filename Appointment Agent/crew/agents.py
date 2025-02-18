import os
from dotenv import load_dotenv
from crewai import Agent
import litellm
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import ChatLiteLLM
from tools import CalendarTool  

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-pro",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")  
)

scheduler_agent = Agent(
    role="Appointment Scheduler",
    goal="Schedule, reschedule, or cancel appointments based on user requests.",
    backstory=(
        "You are an AI assistant specialized in managing appointments. "
        "You interact with users to understand their scheduling needs and "
        "update the calendar accordingly."
    ),
    tools=[CalendarTool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

support_agent = Agent(
    role="Customer Support",
    goal="Provide users with information about their appointments and resolve scheduling conflicts.",
    backstory=(
        "You are a friendly AI assistant who helps users with their appointment-related queries. "
        "You provide clear and concise information and ensure customer satisfaction."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)
