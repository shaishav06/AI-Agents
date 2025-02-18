from crewai import Agent

notifier_agent = Agent(
    role="Notifier",
    goal="Notify users about their upcoming appointments.",
    backstory="An AI agent responsible for sending appointment notifications.",
    tools=[],
    allow_delegation=False,
    verbose=True,
    memory=True,
)
