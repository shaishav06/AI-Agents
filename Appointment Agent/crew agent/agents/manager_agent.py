from crewai import Agent

manager_agent = Agent(
    role="Manager",
    goal="Oversee the scheduling and notification processes.",
    backstory="An AI agent responsible for managing the overall appointment system.",
    tools=[],
    allow_delegation=True,
    verbose=True,
    memory=True,
)
