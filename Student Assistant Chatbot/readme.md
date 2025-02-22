# 📚 Student Assistant Agent

## 🎯 Project Overview
The **Student Assistant Agent** is an AI-powered chatbot built using **Gemini** and **Groq** for answering student queries, providing learning assistance, and offering academic support. The project features:

✅ **AI Models**: Gemini & Groq for intelligent responses  
✅ **Frontend**: Streamlit for a simple web UI  
✅ **Backend**: Python-based API handling requests  
✅ **Modular Codebase**: Organized into `models`, `utils`, and `app.py`  

---

## 📁 Project Structure
```
Student_Assistant_Agent/
│── models/
│   │── gemini_model.py      # Gemini AI model integration
│   │── groq_model.py        # Groq AI model integration
│
│── utils/
│   │── chatbot.py           # Chatbot logic & interaction
│   │── config.py            # Configuration & API keys
│
│── app.py                   # Main Streamlit app
│── requirements.txt          # Dependencies
│── README.md                 # Project Documentation
│── assets/
│   │── landing_page.png      # Screenshot of landing page
```

---

## 🌟 Features
🔹 **AI-driven responses** with Gemini & Groq  
🔹 **User-friendly UI** built with Streamlit  
🔹 **Easy configuration** via `config.py`  
🔹 **Modular structure** for easy extension  

---

## 🔧 Installation & Setup
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-repo/Student-Assistant-Agent.git
cd Student-Assistant-Agent
```

### 2️⃣ **Create & Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Set Up API Keys**
Edit `utils/config.py` and add your API keys:
```python
GEMINI_API_KEY = "your_gemini_api_key"
GROQ_API_KEY = "your_groq_api_key"
```

### 5️⃣ **Run the Application**
```bash
streamlit run app.py
```

---

## 🎥 Landing Page Screenshot

![Landing Page](https://raw.githubusercontent.com/shaishav06/AI-Agents/main/Student%20Assistant%20Chatbot/Screenshot%20from%202025-02-22%2014-44-38.png)

---

## 🚀 Usage
1️⃣ **Open the Streamlit App**  
2️⃣ **Enter your query** in the text box  
3️⃣ **Select AI Model** (Gemini or Groq)  
4️⃣ **Get AI-powered responses** instantly  

---

## 🤝 Contributing
Feel free to submit **issues** or **pull requests** to enhance the Student Assistant Agent.

📧 Contact: shaishavsurati06@gmail.com

---

## 📜 License
MIT License © 2025 Student Assistant Team

