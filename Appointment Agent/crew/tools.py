from langchain_core.tools import StructuredTool
from typing import Literal

def calendar_tool(action: Literal["schedule", "reschedule", "cancel", "get_info"], details: str) -> str:
    """A tool to manage appointments in a calendar."""
    if action == "schedule":
        return f"✅ Appointment scheduled: {details}"
    elif action == "reschedule":
        return f"🔄 Appointment rescheduled: {details}"
    elif action == "cancel":
        return f"❌ Appointment canceled: {details}"
    elif action == "get_info":
        return f"📅 Appointment details: {details}"
    else:
        return "⚠️ Invalid action."

CalendarTool = StructuredTool.from_function(
    func=calendar_tool,
    name="calendar_tool",
    description="Handles scheduling, rescheduling, canceling, and retrieving appointment information.",
)
