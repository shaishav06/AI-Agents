import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import GOOGLE_SHEET_ID

SERVICE_ACCOUNT_FILE = "credentials.json"  # Ensure this file is in the project root
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def save_to_google_sheets(data):
    """Append extracted leads to Google Sheets."""
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    
    values = [[lead["name"], lead["email"], lead["company"], lead["profile_url"]] for lead in data]
    body = {"values": values}
    
    result = sheet.values().append(
        spreadsheetId=GOOGLE_SHEET_ID,
        range="Sheet1!A:D",
        valueInputOption="RAW",
        body=body
    ).execute()
    
    print(f"{result.get('updates').get('updatedCells')} cells updated.")
