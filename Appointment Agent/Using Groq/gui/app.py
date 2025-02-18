# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from agents.groq_agent import GroqAgent
# from agents.gemini_agent import GeminiAgent


# import streamlit as st
# from agents.groq_agent import GroqAgent
# from agents.gemini_agent import GeminiAgent

# # Initialize agents
# groq_agent = GroqAgent()
# gemini_agent = GeminiAgent()

# # Streamlit UI
# st.title("📅 AI Appointment Scheduler")

# query = st.text_input("Ask something about your appointment:")
# if st.button("Get Answer"):
#     if query:
#         response = groq_agent.answer_query(query)
#         st.write("🤖 AI Response:", response)
#     else:
#         st.warning("Please enter a query.")

# appointment_details = st.text_area("Enter appointment details:")
# if st.button("Schedule Appointment"):
#     if appointment_details:
#         confirmation = gemini_agent.schedule_appointment(appointment_details)
#         st.success("✅ Appointment Scheduled!")
#         st.write("📩 Confirmation:", confirmation)
#     else:
#         st.warning("Please enter appointment details.")

# import streamlit as st
# from utils.database import store_appointment, get_appointments

# st.title("🗓️ AI Appointment Scheduler")

# # Form for scheduling an appointment
# with st.form("appointment_form"):
#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     date = st.date_input("Appointment Date")
#     time = st.time_input("Appointment Time")
#     reason = st.text_area("Reason for Appointment")
#     submit_button = st.form_submit_button("Schedule Appointment")

#     if submit_button:
#         if name and email and date and time:
#             store_appointment(name, email, str(date), str(time), reason)
#             st.success(f"Appointment scheduled for {name} on {date} at {time} ✅")
#         else:
#             st.error("Please fill in all required fields!")

# # Display scheduled appointments
# st.subheader("📋 Scheduled Appointments")
# appointments = get_appointments()
# if appointments:
#     for appointment in appointments:
#         st.write(f"🟢 **{appointment[1]}** - {appointment[3]} {appointment[4]} ({appointment[2]})")
# else:
#     st.info("No appointments scheduled yet.")


import streamlit as st
from utils.database import create_connection, create_table, store_appointment, get_appointments
from utils.gemini_integration import generate_gemini_content
from utils.groq_integration import generate_groq_content

# Initialize database
db_file = "appointments.db"
conn = create_connection(db_file)
create_table(conn)

st.title("Appointment Scheduler with AI Integration")

# Appointment form
st.header("Schedule a New Appointment")
with st.form("appointment_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    appointment_date = st.date_input("Appointment Date")
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Schedule Appointment")

    if submitted:
        if name and email and appointment_date:
            appointment = (name, email, str(appointment_date), notes)
            store_appointment(conn, appointment)
            st.success("Appointment scheduled successfully.")
        else:
            st.error("Please fill in all required fields.")

# Display appointments
st.header("Scheduled Appointments")
appointments = get_appointments(conn)
for appt in appointments:
    st.write(f"**Name:** {appt[1]}")
    st.write(f"**Email:** {appt[2]}")
    st.write(f"**Date:** {appt[3]}")
    st.write(f"**Notes:** {appt[4]}")
    st.write("---")

# AI Content Generation
st.header("AI Content Generation")
prompt = st.text_area("Enter a prompt for AI content generation:")
if st.button("Generate with Gemini"):
    if prompt:
        result = generate_gemini_content(prompt)
        st.write("**Gemini Response:**")
        st.write(result)
    else:
        st.error("Please enter a prompt.")
if st.button("Generate with Groq"):
    if prompt:
        result = generate_groq_content(prompt)
        st.write("**Groq Response:**")
        st.write(result)
    else:
        st.error("Please enter a prompt.")
