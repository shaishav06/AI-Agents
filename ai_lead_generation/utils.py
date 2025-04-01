def clean_data(leads):
    """Format and clean extracted lead data."""
    cleaned_leads = []
    for lead in leads:
        if "email" in lead and lead["email"]:
            cleaned_leads.append({
                "name": lead.get("name", "N/A"),
                "email": lead.get("email", "N/A"),
                "company": lead.get("company", "N/A"),
                "profile_url": lead.get("profile_url", "N/A"),
            })
    return cleaned_leads
