import os
from dotenv import load_dotenv
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit App Title
st.title("Gemini-CrewAI Agent")
st.write("This app uses CrewAI agents to research and write about the latest advancements in AI.")

# Input for user query
user_query = st.text_input("Enter a topic to research (e.g., 'What is AI Agent?'):")

if user_query:
    # Define the search tool
    search_tool = DuckDuckGoSearchRun()

    # Define your agents
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Uncover cutting-edge developments in AI and data science',
        backstory="""You work at a leading tech think tank.
        Your expertise lies in identifying emerging trends.
        You have a knack for dissecting complex data and presenting actionable insights.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    )

    writer = Agent(
        role='Tech Content Strategist',
        goal='Craft compelling content on tech advancements',
        backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
        You transform complex concepts into compelling narratives.""",
        verbose=True,
        llm=ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY),
        allow_delegation=True
    )

    # Create tasks for your agents
    task1 = Task(
        description=f"""Conduct a comprehensive analysis of {user_query}.
        Identify key trends, breakthrough technologies, and potential industry impacts.""",
        expected_output="Full analysis report in bullet points",
        agent=researcher
    )

    task2 = Task(
        description=f"""Using the insights provided, develop an engaging blog post about {user_query}.
        Your post should be informative yet accessible, catering to a tech-savvy audience.
        Make it sound cool, avoid complex words so it doesn't sound like AI.""",
        expected_output="Full blog post of at least 4 paragraphs",
        agent=writer
    )

    # Instantiate your crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2
    )

    # Run the crew and display results
    if st.button("Run Analysis"):
        with st.spinner("Running analysis and generating content..."):
            result = crew.kickoff()
            st.success("Analysis Complete!")
            st.write("### Research Report")
            st.write(result)