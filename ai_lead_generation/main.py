import os
import json
import requests
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import ollama
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Firecrawl API configuration
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
FIRECRAWL_BASE_URL = os.getenv("FIRECRAWL_BASE_URL")

# Google Sheets configuration
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

# Get the credentials file path from environment variable
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Ollama configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "0.0.0.0:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")

class LeadGenerator:
    def __init__(self):
        # Initialize Ollama client
        self.ollama_base_url = f"http://{OLLAMA_URL}"
        
        # Set up Firecrawl headers
        self.firecrawl_headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Set up Google Sheets client
        self.setup_google_sheets()

    def setup_google_sheets(self):
        try:
            # Use credentials.json for Google Sheets API authentication
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            
            # Try to use the path from environment variable first
            if os.path.exists(GOOGLE_CREDENTIALS_PATH):
                creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
            # Fall back to credentials.json in current directory if env variable path doesn't exist
            elif os.path.exists("credentials.json"):
                creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            else:
                raise FileNotFoundError("Google credentials file not found. Please check your GOOGLE_APPLICATION_CREDENTIALS path or ensure credentials.json exists in the current directory.")
            
            self.gc = gspread.authorize(creds)
            
            # Open the spreadsheet
            self.spreadsheet = self.gc.open_by_key(GOOGLE_SHEET_ID)
            
            # Try to open the worksheet, create it if it doesn't exist
            try:
                self.sheet = self.spreadsheet.worksheet(SHEET_NAME)
            except gspread.exceptions.WorksheetNotFound:
                # Create the worksheet if it doesn't exist
                self.sheet = self.spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=20)
                st.info(f"Created new worksheet '{SHEET_NAME}'")
            
            # Initialize the sheet with headers if it's empty
            if not self.sheet.get_all_values():
                headers = [
                    "Date Added", "Source", "Name", "Title", "Company", 
                    "Email", "Phone", "LinkedIn", "Twitter", "Website", 
                    "Industry", "Keywords", "Discussion Context", "Lead Score", "Notes"
                ]
                self.sheet.append_row(headers)
                
        except FileNotFoundError as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure your credentials.json file exists and has proper Google Sheets API access")
        except Exception as e:
            st.error(f"Error setting up Google Sheets: {str(e)}")
            st.info("Check your Google Sheet ID and make sure your service account has access to it")

    def search_discussions(self, keywords, sources=None, max_results=50):
        """Search online discussions using Firecrawl API"""
        try:
            endpoint = f"{FIRECRAWL_BASE_URL}/search"
            
            # Build the payload
            payload = {
                "query": keywords,
                "max_results": max_results
            }
            
            if sources:
                payload["sources"] = sources
                
            # Make the API request
            response = requests.post(endpoint, headers=self.firecrawl_headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Firecrawl API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error searching discussions: {str(e)}")
            return None

    def extract_lead_info(self, discussion_data):
        """Extract potential lead information from discussion data using Ollama"""
        leads = []
        
        for discussion in discussion_data.get("results", []):
            context = discussion.get("text", "")
            source_url = discussion.get("url", "")
            source_name = discussion.get("source", "Unknown")
            
            # Skip if context is too short
            if len(context) < 50:
                continue
                
            # Use Ollama to extract lead information
            prompt = f"""
            Extract potential lead information from this online discussion:
            
            Discussion: {context}
            Source: {source_url}
            
            Extract any potential leads with the following information (return JSON only):
            {{
                "leads": [
                    {{
                        "name": "Full name of the person if mentioned",
                        "title": "Job title if mentioned",
                        "company": "Company name if mentioned",
                        "email": "Email if mentioned",
                        "phone": "Phone if mentioned",
                        "linkedin": "LinkedIn profile if mentioned",
                        "twitter": "Twitter handle if mentioned",
                        "website": "Website if mentioned", 
                        "industry": "Industry if mentioned",
                        "keywords": "Relevant keywords from discussion",
                        "lead_score": "Score from 1-10 based on potential value as a lead"
                    }}
                ]
            }}
            
            Only extract people who appear to be potential clients or decision-makers. If no leads are identified, return an empty array. Return valid JSON only.
            """
            
            try:
                # Call Ollama model
                response = ollama.chat(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    host=self.ollama_base_url
                )
                
                # Extract the response text
                ai_response = response["message"]["content"]
                
                # Parse the JSON response
                # Find JSON in the response (in case model adds extra text)
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = ai_response[json_start:json_end]
                    try:
                        extracted_data = json.loads(json_str)
                        
                        # Add source information to each lead
                        for lead in extracted_data.get("leads", []):
                            lead["source"] = source_name
                            lead["source_url"] = source_url
                            lead["discussion_context"] = context[:500] + "..." if len(context) > 500 else context
                            leads.append(lead)
                            
                    except json.JSONDecodeError as je:
                        st.warning(f"Failed to parse JSON from model response: {str(je)}")
                        continue
            
            except Exception as e:
                st.warning(f"Error extracting lead info: {str(e)}")
                continue
                
        return leads

    def save_leads_to_sheet(self, leads):
        """Save the extracted leads to Google Sheets"""
        if not leads:
            return 0
            
        count = 0
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for lead in leads:
            try:
                # Prepare row data
                row = [
                    current_date,
                    lead.get("source", ""),
                    lead.get("name", ""),
                    lead.get("title", ""),
                    lead.get("company", ""),
                    lead.get("email", ""),
                    lead.get("phone", ""),
                    lead.get("linkedin", ""),
                    lead.get("twitter", ""),
                    lead.get("website", ""),
                    lead.get("industry", ""),
                    lead.get("keywords", ""),
                    lead.get("discussion_context", ""),
                    lead.get("lead_score", ""),
                    ""  # Notes (empty by default)
                ]
                
                # Check if lead already exists (by name, company and email)
                existing_data = self.sheet.get_all_values()
                
                # Skip header row
                existing_data = existing_data[1:] if existing_data else []
                
                # Check if lead already exists
                already_exists = False
                for existing_row in existing_data:
                    if len(existing_row) >= 6:  # Make sure row has enough elements
                        if (lead.get("name", "") and lead.get("name", "") == existing_row[2] and 
                            lead.get("company", "") and lead.get("company", "") == existing_row[4] and
                            lead.get("email", "") and lead.get("email", "") == existing_row[5]):
                            already_exists = True
                            break
                
                if not already_exists:
                    self.sheet.append_row(row)
                    count += 1
                    time.sleep(1)  # Avoid Google Sheets API quota limits
            
            except Exception as e:
                st.error(f"Error saving lead to sheet: {str(e)}")
                continue
                
        return count

def main():
    st.set_page_config(page_title="AI Lead Generation Agent", layout="wide")
    
    st.title("AI Lead Generation Agent")
    st.subheader("Find potential clients in online discussions")
    
    # Initialize the lead generator
    lead_generator = LeadGenerator()
    
    # Sidebar for configuration
    st.sidebar.header("Search Configuration")
    
    # Keywords input
    keywords = st.sidebar.text_area("Enter keywords to search for (e.g., 'looking for marketing agency', 'need web development')", 
                                    height=100)
    
    # Source selection
    source_options = [
        "reddit", "hackernews", "twitter", "medium", "dev.to", 
        "producthunt", "indiehackers"
    ]
    selected_sources = st.sidebar.multiselect(
        "Select sources to search (optional)",
        options=source_options
    )
    
    # Max results slider
    max_results = st.sidebar.slider("Maximum results to fetch", 10, 200, 50)
    
    # Run button
    if st.sidebar.button("Generate Leads"):
        if not keywords:
            st.warning("Please enter keywords to search for.")
            return
            
        with st.spinner("Searching for discussions..."):
            # Step 1: Search for discussions
            search_results = lead_generator.search_discussions(
                keywords=keywords,
                sources=selected_sources if selected_sources else None,
                max_results=max_results
            )
            
            if not search_results:
                st.error("No search results found. Try different keywords or sources.")
                return
                
            st.success(f"Found {len(search_results.get('results', []))} discussions")
            
            # Step 2: Extract lead information
            with st.spinner("Extracting lead information using AI..."):
                leads = lead_generator.extract_lead_info(search_results)
                
            if not leads:
                st.warning("No potential leads were identified in the discussions.")
                return
                
            st.success(f"Extracted {len(leads)} potential leads")
            
            # Step 3: Save to Google Sheets
            with st.spinner("Saving leads to Google Sheets..."):
                saved_count = lead_generator.save_leads_to_sheet(leads)
                
            st.success(f"Successfully saved {saved_count} new leads to Google Sheets")
            
            # Display the leads in a table
            leads_df = pd.DataFrame(leads)
            st.subheader("Extracted Leads")
            st.dataframe(leads_df)
            
            # Add a link to the Google Sheet
            sheet_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}"
            st.markdown(f"[Open Google Sheet]({sheet_url})")
    
    # Display instructions
    with st.expander("How to use this tool"):
        st.markdown("""
        ### AI Lead Generation Agent Instructions
        
        1. **Enter keywords** in the sidebar to search for potential clients. Good examples:
           - "looking for marketing agency"
           - "need help with website development"
           - "seeking consulting services for SEO"
           
        2. **Select sources** where you want to search for discussions (optional).
        
        3. **Set the maximum results** to control how many discussions to analyze.
        
        4. **Click "Generate Leads"** to start the process.
        
        5. The agent will:
           - Search online discussions using Firecrawl API
           - Extract potential lead information using AI
           - Save the leads to your Google Sheet
           - Display the results in this interface
           
        ### Setup Requirements
        
        1. Ensure you have a `credentials.json` file with Google Sheets API access.
        2. Make sure the Google Sheet exists and has the correct sheet name.
        3. The Ollama model must be running at the configured URL.
        """)

if __name__ == "__main__":
    main()