from crewai import Crew, Process
from agents import scheduler_agent, support_agent
from tasks import schedule_task, reschedule_task, cancel_task, info_task

class AppointmentCrew:
    def __init__(self, action, details):
        self.action = action
        self.details = details

    def run(self):
        task_map = {
            "schedule": (scheduler_agent, schedule_task),
            "reschedule": (scheduler_agent, reschedule_task),
            "cancel": (scheduler_agent, cancel_task),
            "info": (support_agent, info_task),
        }

        if self.action not in task_map:
            raise ValueError("Invalid action.")

        agent, task = task_map[self.action]
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
        )

        result = crew.kickoff(inputs={"details": self.details})
        return result
