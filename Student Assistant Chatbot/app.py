import streamlit as st
from utils.chatbot import StudentAssistantAgent

# Initialize the chatbot
agent = StudentAssistantAgent()

st.title("🎓 Student Assistant Chatbot")
st.write("An AI-driven chatbot for academic support using Gemini, Groq.")

# User Input
user_input = st.text_input("Ask me anything about your studies:")
option = st.selectbox("Choose Assistance Type:", 
                      ["Retrieve Study Materials", "Answer Query", "Generate Study Plan"])

if st.button("Submit"):
    if user_input:
        if option == "Retrieve Study Materials":
            result = agent.retrieve_study_materials(user_input)
        elif option == "Answer Query":
            result = agent.answer_query(user_input)
        else:
            result = agent.generate_study_plan(user_input)

        st.write("### Response:")
        st.write(result)
    else:
        st.warning("Please enter a query.")
