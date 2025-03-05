
---

# **Copy Editor AI Agent**  
AI-powered tool to enhance the clarity and effectiveness of webpage content using **Gemini AI** and **Groq AI**.

## **Features**  
✅ Analyze webpage content for clarity and effectiveness.  
✅ Provide improvement suggestions using **Gemini AI** or **Groq AI**.  
✅ Extract text from URLs and generate AI-powered feedback.  
✅ User-friendly **Streamlit UI** for easy interaction.  

---

## **Installation & Setup**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/copy-editor-ai.git
cd copy-editor-ai
```

### **2. Create & Activate Virtual Environment**  
```bash
python3 -m venv .venv
source .venv/bin/activate  # For macOS/Linux
# or
.venv\Scripts\activate     # For Windows
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Set Up API Keys**  
Create a **.env** file in the project root and add your API keys:  
```
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## **Usage**  

### **Run the AI Copy Editor Agent**  
```bash
streamlit run app.py
```

1. Open the **web interface** (URL shown in the terminal).  
2. Enter a webpage URL to analyze.  
3. Choose **Gemini AI** or **Groq AI** for content improvement suggestions.  
4. Click **"Analyze Content"** to get AI-generated feedback.  

---

## **Project Structure**  
```
📂 copy-editor-ai
│── 📄 app.py          # Streamlit app entry point
│── 📄 frontend.py     # UI logic for AI selection and text analysis
│── 📄 ai_agent.py     # AI logic using Gemini & Groq
│── 📄 scraper.py      # Extracts text from webpage URLs
│── 📄 requirements.txt # Required dependencies
│── 📄 .env            # API keys (ignored in Git)
│── 📄 README.md       # Documentation
```

---

## **Requirements** (requirements.txt)  
```
streamlit
python-dotenv
google-generativeai
groq
requests
beautifulsoup4
```

---

## **Contributing**  
Feel free to fork the repository and contribute!  

1. **Fork the repo**  
2. **Create a feature branch** (`git checkout -b feature-name`)  
3. **Commit changes** (`git commit -m "Added new feature"`)  
4. **Push to GitHub** (`git push origin feature-name`)  
5. **Create a Pull Request**  

---

## **License**  
📜 MIT License – Free to use and modify.  

---

### 🚀 **Now you're ready to enhance webpage content with AI!** 🎉