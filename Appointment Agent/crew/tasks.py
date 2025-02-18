from crewai import Task
from agents import scheduler_agent, support_agent

schedule_task = Task(
    description="Schedule an appointment for the user based on their preferred date and time.",
    expected_output="A confirmation message with the appointment details.",
    agent=scheduler_agent,
)

reschedule_task = Task(
    description="Reschedule an existing appointment for the user.",
    expected_output="A confirmation message with the updated appointment details.",
    agent=scheduler_agent,
)

cancel_task = Task(
    description="Cancel an existing appointment for the user.",
    expected_output="A confirmation message for the cancellation.",
    agent=scheduler_agent,
)

info_task = Task(
    description="Provide details about the user's upcoming appointments.",
    expected_output="A summary of the user's appointments.",
    agent=support_agent,
)
