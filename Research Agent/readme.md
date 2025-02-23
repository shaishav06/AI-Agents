# Research Agent

This project is a **Research Agent** built with **Gemini** and **CrewAI**, featuring a **Streamlit** frontend. The agent conducts research on AI advancements and generates insightful content.

## 🚀 Features
- Uses **Gemini Pro** for advanced AI responses
- **CrewAI agents** for research and content generation
- **DuckDuckGo Search Tool** for fetching up-to-date information
- **Streamlit UI** for user interaction

## 📂 Project Structure
```
Research-Agent/
│── requirements.txt
│── gemini-crewai-Agent.py
```

## 🛠 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Research-Agent.git
cd Research-Agent
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys
Create a `.env` file in the project directory and add your **Google API Key**:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 Running the App
```bash
streamlit run gemini-crewai-Agent.py
```

## 📸 Landing Page Screenshot
![Landing Page](./landing_page.png)

## 🧠 How It Works
1. **User Input**: Enter a topic to research (e.g., "What is AI Agent?").
2. **CrewAI Agents**:
   - **Researcher Agent**: Finds the latest advancements.
   - **Writer Agent**: Creates an engaging blog post.
3. **Streamlit Interface**: Displays the research and blog output.

## 🤖 Technologies Used
- **Gemini Pro (Google AI)**
- **CrewAI** (for multi-agent collaboration)
- **LangChain** (to integrate AI models)
- **Streamlit** (frontend for user interaction)
- **DuckDuckGo Search Tool** (fetches up-to-date research data)

## 🎯 Future Enhancements
- Add **PDF export** for research reports
- Support for **multiple AI models**
- Improve **agent memory & reasoning**

---
Made with ❤️ by **[@shaishav06]**

