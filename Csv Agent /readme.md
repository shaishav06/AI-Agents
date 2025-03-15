# LangChain CSV Analysis Agent with Groq LLM

## Introduction
This repository provides a Jupyter notebook that implements an intelligent CSV analysis system using LangChain and the Groq LLM (llama-3.3-70b-versatile model). The system allows users to query the dataset conversationally without writing explicit code.

## Features
- AI-powered CSV data analysis using **LangChain** and **Groq LLM**
- Supports **natural language queries** on salary data (`salaries_2023.csv`)
- Custom prompt engineering to enhance accuracy
- Verification methods to reduce hallucination
- Interactive interface through **Python** and **Streamlit** (commented out for now)

## Installation
To use this project, install the required dependencies:

```bash
pip install -qU pyodbc tabulate langchain langchain-community langchain-core langchain-experimental groq pandas
```

## Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/csv-agent.git
   cd csv-agent
   ```
2. Open the **Jupyter notebook** and run it step by step.
3. Modify the **CSV file path** in the script if needed.
4. Use the AI agent to analyze salary data with natural language queries.

## Example Query
Ask a question like:
```python
QUESTION = "Which department makes the most on average and give the actual amount?"
res = agent.invoke(CSV_PROMPT_PREFIX + QUESTION + CSV_PROMPT_SUFFIX)
print(res["output"])
```

## Contribution
Contributions are welcome! Feel free to **fork** this repository, make improvements, and submit a **pull request**.

## Contact
- **GitHub**: [shaishav06](https://github.com/shaishav06)
- **LinkedIn**: [Shaishav Surati 🇮🇳](https://www.linkedin.com/in/shaishavsurati)
- **Email**: shaishavsurati06@gmail.com

---
🚀 Happy coding!

