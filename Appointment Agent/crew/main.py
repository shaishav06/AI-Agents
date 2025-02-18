import streamlit as st
from crew import AppointmentCrew

# Streamlit App Title
st.title("📅 Appointment Scheduling AI Agent")
st.write("Schedule, reschedule, cancel, or get info about your appointments.")

# User Input
action = st.selectbox("What would you like to do?", ["Schedule", "Reschedule", "Cancel", "Get Info"])
details = st.text_area("Provide details (e.g., date, time, reason):")

# Run the Crew
if st.button("Submit"):
    if not details:
        st.error("⚠️ Please provide details!")
    else:
        with st.spinner("🤖 Processing your request..."):
            # Map user-friendly action names to function names
            action_map = {
                "Schedule": "schedule",
                "Reschedule": "reschedule",
                "Cancel": "cancel",
                "Get Info": "info",
            }
            crew = AppointmentCrew(action=action_map[action], details=details)
            result = crew.run()
            st.success("✅ Done!")
            st.write("### Result")
            st.write(result)
