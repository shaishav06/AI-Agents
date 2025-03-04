import streamlit as st
from ai_agent import get_gemini_feedback, get_groq_feedback
from scraper import extract_text_from_url

def main():
    st.title("Webpage Copy Editor AI")

    st.subheader("Enhance clarity and effectiveness of webpage content!")

    option = st.selectbox("Choose AI Model", ["Gemini", "Groq"])

    url = st.text_input("Enter Webpage URL:")

    if st.button("Analyze Content"):
        with st.spinner("Fetching and analyzing..."):
            webpage_text = extract_text_from_url(url)
            if "Error" in webpage_text:
                st.error(webpage_text)
                return

            if option == "Gemini":
                response = get_gemini_feedback(webpage_text)
            else:
                response = get_groq_feedback(webpage_text)

        st.subheader(f"AI ({option}) Suggestions:")
        st.write(response)

if __name__ == "__main__":
    main()
