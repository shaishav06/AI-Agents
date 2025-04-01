from utils.firecrawl import search_leads
from utils.ollama_model import extract_lead_info
from utils.gsheet import write_to_sheet

def main():
    query = "AI startups looking for automation solutions"
    
    print("🔍 Searching for leads...")
    leads = search_leads(query, limit=5)

    structured_data = []
    for lead in leads:
        extracted_info = extract_lead_info(lead["content"])
        structured_data.append([lead["source"], extracted_info])

    print("📊 Saving to Google Sheets...")
    write_to_sheet(structured_data)

    print("✅ Lead Generation Completed!")

if __name__ == "__main__":
    main()
