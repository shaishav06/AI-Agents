# AI Lead Generation Agent

This tool automatically finds potential clients in online discussions, extracts their profiles and contact information, and organizes everything in Google Sheets. It uses:

- **Firecrawl API** to search online discussions
- **Ollama** (llama3.2 model) to extract lead information
- **Google Sheets API** to store and organize leads
- **Streamlit** for the user interface

## Features

- 🔍 Search multiple platforms for relevant discussions (Reddit, HackerNews, Twitter, etc.)
- 🤖 AI-powered extraction of lead information from discussions
- 📊 Automatic organization of leads in Google Sheets
- 🏆 Lead scoring to prioritize high-value prospects
- 🚀 Easy-to-use interface with Streamlit

## Requirements

- Python 3.8+
- Ollama with llama3.2 model installed
- Firecrawl API key
- Google Sheets API credentials

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/lead-generation-agent.git
   cd lead-generation-agent
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```
   FIRECRAWL_API_KEY="your-firecrawl-api-key"
   FIRECRAWL_BASE_URL="https://api.firecrawl.dev/"
   GOOGLE_SHEET_ID="your-google-sheet-id"
   OLLAMA_PATH='/usr/local/bin/'
   OLLAMA_URL='0.0.0.0:11434'
   OLLAMA_ORIGINS='*'
   MODEL_NAME="llama3.2"
   SHEET_NAME="Lead_Generation"
   ```

4. Set up Google Sheets API:
   - Create a service account in Google Cloud Console
   - Download the credentials.json file
   - Share your Google Sheet with the service account email
   - Create a worksheet named "Lead_Generation" in your Google Sheet

## Usage

1. Start Ollama server with the llama3.2 model:
   ```
   ollama serve
   ```

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Open your browser at http://localhost:8501

4. Enter keywords to search for potential clients, select sources, and click "Generate Leads"

## Project Structure

- `main.py`: Core functionality for lead generation
- `app.py`: Streamlit interface
- `requirements.txt`: Python dependencies
- `.env`: Configuration file
- `credentials.json`: Google API credentials (you need to create this)

## Google Sheets Setup

The app will automatically create the following columns in your Google Sheet:

- Date Added
- Source
- Name
- Title
- Company
- Email
- Phone
- LinkedIn
- Twitter
- Website
- Industry
- Keywords
- Discussion Context
- Lead Score
- Notes

## License

MIT

## Acknowledgements

- This project uses the Firecrawl API for searching online discussions
- Lead extraction is powered by the llama3.2 model via Ollama
- Frontend built with Streamlit