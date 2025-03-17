# Salary Analysis Assistant using OpenAI's Assistants API

## Introduction
This project implements an intelligent **Salary Analysis Assistant** using OpenAI's Assistants API and Thread Management. The system is designed to process and analyze employee salary data stored in a **SQLite database**, providing automated responses to salary-related queries through natural language interaction.

## Features
- Uses **OpenAI Assistants API** for handling salary-related queries.
- Implements **thread-based conversation management**.
- Connects to a **SQLite database** to retrieve salary data.
- Provides automated responses using **custom helper functions**.
- Supports **real-time function calling** and response handling.

## Prerequisites
Before running the project, ensure you have the following:
- **Python 3.8+** installed
- **OpenAI API Key**
- Required Python packages:
  ```bash
  pip install -qU pyodbc tabulate langchain langchain-community langchain-core langchain-experimental langchain-openai SQLAlchemy pandas
  ```
- Access to a **salary database (SQLite)**

## Setup & Usage
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/salary-analysis-assistant.git
   cd salary-analysis-assistant
   ```
2. **Set Up Environment Variables**
   - Store your **OpenAI API Key** in the environment:
     ```python
     import os
     os.environ['OPENAI_API_KEY'] = "your-api-key"
     ```
3. **Prepare the Salary Database**
   - Upload your `salaries_2023.csv` file to the `/db` folder.
   - The script will automatically load the data into the SQLite database.

4. **Run the Assistant**
   ```python
   python salary_assistant.py
   ```

## How It Works
- The assistant is initialized using **OpenAI's Assistants API**.
- It interacts with the **SQLite database** using SQLAlchemy.
- It processes user queries related to salaries and retrieves data accordingly.
- The responses are generated dynamically based on the database content.

## Contributing
Contributions are welcome! If you're interested in improving this project:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## Contact
For questions or contributions, feel free to reach out:
- **GitHub:** [shaishav06](https://github.com/shaishav06)
- **LinkedIn:** [Shaishav Surati 🇮🇳](https://linkedin.com/in/shaishavsurati)
- **Email:** shaishavsurati06@gmail.com

## License
This project is licensed under the MIT License.

