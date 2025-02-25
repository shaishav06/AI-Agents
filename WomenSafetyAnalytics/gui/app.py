import streamlit as st
from utils.data_processing import load_crime_data, preprocess_data, extract_features
from utils.groq_integration import analyze_text_with_groq
from utils.gemini_integration import analyze_text_with_gemini
from models.risk_assessment import train_risk_model, predict_risk
from models.alert_system import send_alert

# Load and preprocess data
crime_data = load_crime_data('data/crime_reports.csv')
processed_data = preprocess_data(crime_data)
features = extract_features(processed_data)

# Placeholder for model training (implement as needed)
# model = train_risk_model(features, labels)

st.title("Women Safety Analytics")

# User input
st.header("Input Text or Voice")
user_input = st.text_area("Enter your text here:")

if st.button("Analyze with Groq"):
    if user_input:
        result = analyze_text_with_groq(user_input)
        st.write("**Groq Analysis Result:**")
        st.write(result)
    else:
        st.error("Please enter some text.")

if st.button("Analyze with Gemini"):
    if user_input:
        result = analyze_text_with_gemini(user_input)
        st.write("**Gemini Analysis Result:**")
        st.write(result)
    else:
        st.error("Please enter some text.")

# Placeholder for risk prediction (implement as needed)
# risk_level = predict_risk(model, new_features)
# st.write(f"Predicted Risk Level: {risk_level}")

# Placeholder for sending alerts (implement as needed)
# send_alert(user_contact, alert_message)
