import streamlit as st
import sqlite3
from agents.scheduler_agent import scheduler_agent
from agents.notifier_agent import notifier_agent
from agents.manager_agent import manager_agent
from tools.groq_tool import generate_groq_response
from tools.gemini_tool import generate_gemini_response

# Initialize database
conn = sqlite3.connect('data/appointments.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        notes TEXT
    )
''')
conn.commit()

st.title("AI-Powered Appointment Scheduler")

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
            c.execute('INSERT INTO appointments (name, email, appointment_date, notes) VALUES (?, ?, ?, ?)',
                      (name, email, str(appointment_date), notes))
            conn.commit()
            st.success("Appointment scheduled successfully.")
        else:
            st.error("Please fill in all required fields.")

# Display appointments
st.header("Scheduled Appointments")
c.execute('SELECT * FROM appointments')
appointments = c.fetchall()
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
        result = generate_gemini_response(prompt)
        st.write("**Gemini Response:**")
        st.write(result)
    else:
        st.error("Please enter a prompt.")
if st.button("Generate with Groq"):
    if prompt:
        result = generate_groq_response(prompt)
        st.write("**Groq Response:**")
        st.write(result)
    else:
        st.error("Please enter a prompt.")
