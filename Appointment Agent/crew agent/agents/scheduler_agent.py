from crewai import Agent

scheduler_agent = Agent(
    role="Scheduler",
    goal="Manage and schedule appointments efficiently.",
    backstory="An AI agent responsible for handling appointment scheduling.",
    tools=[],
    allow_delegation=True,
    verbose=True,
    memory=True,
)
