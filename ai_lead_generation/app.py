import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv
from main import LeadGenerator

# Load environment variables
load_dotenv()

# Constants from environment
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

# Set page configuration
st.set_page_config(
    page_title="AI Lead Generation Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #E8F5E9;
        border-radius: 0.5rem;
        border-left: 5px solid #4CAF50;
    }
    .info-box {
        padding: 1rem;
        background-color: #E3F2FD;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stProgress .st-eb {
        background-color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown('<div class="main-header">🤖 AI Lead Generation Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Find potential clients in online discussions</div>', unsafe_allow_html=True)

# Initialize session state for storing leads
if 'leads' not in st.session_state:
    st.session_state.leads = []
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'saved_count' not in st.session_state:
    st.session_state.saved_count = 0

# Initialize the lead generator
@st.cache_resource
def get_lead_generator():
    return LeadGenerator()

try:
    lead_generator = get_lead_generator()
    setup_success = True
except Exception as e:
    st.error(f"Error initializing Lead Generator: {str(e)}")
    st.info("Please check your configuration and try again.")
    setup_success = False

# Only show the main UI if setup was successful
if setup_success:
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔍 Search Configuration")
        
        # Keywords input with examples
        st.subheader("Search Keywords")
        keywords_examples = [
            "looking for marketing agency",
            "need help with web development",
            "seeking consulting services",
            "recommend software for project management",
            "alternatives to [competitor product]"
        ]
        selected_example = st.selectbox("Example searches (select to use)", [""] + keywords_examples)
        
        if selected_example:
            keywords = selected_example
        else:
            keywords = ""
            
        keywords = st.text_area("Enter keywords to search for:", value=keywords, height=100,
                               help="Use specific phrases potential clients might use when looking for your services")
        
        # Source selection
        st.subheader("Sources")
        source_options = [
            "reddit", "hackernews", "twitter", "medium", "dev.to", 
            "producthunt", "indiehackers"
        ]
        selected_sources = st.multiselect(
            "Select sources to search (optional)",
            options=source_options,
            default=["reddit", "hackernews", "twitter"],
            help="Leave empty to search all available sources"
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            max_results = st.slider("Maximum results to fetch", 10, 200, 50, 
                                   help="Higher values may take longer to process")
            min_score = st.slider("Minimum lead score", 1, 10, 5, 
                                 help="Filter leads by AI-determined quality score")
        
        # Run button
        search_button = st.button("🔍 Generate Leads", type="primary", use_container_width=True)

    # Main content area
    if search_button:
        if not keywords:
            st.warning("⚠️ Please enter keywords to search for.")
        else:
            # Display progress using tabs for each step
            tabs = st.tabs(["1. Search Discussions", "2. Extract Leads", "3. Save to Sheets"])
            
            # Step 1: Search for discussions
            with tabs[0]:
                with st.spinner("🔍 Searching for discussions..."):
                    search_results = lead_generator.search_discussions(
                        keywords=keywords,
                        sources=selected_sources if selected_sources else None,
                        max_results=max_results
                    )
                    
                    if not search_results or len(search_results.get('results', [])) == 0:
                        st.error("❌ No discussions found. Try different keywords or sources.")
                        st.stop()
                        
                    result_count = len(search_results.get('results', []))
                    st.success(f"✅ Found {result_count} discussions")
                    
                    # Show sample of discussions
                    st.subheader("Sample discussions:")
                    for i, result in enumerate(search_results.get('results', [])[:3]):
                        with st.expander(f"Discussion {i+1} from {result.get('source', 'Unknown')}"):
                            st.markdown(f"**Source URL:** [{result.get('url', 'N/A')}]({result.get('url', '#')})")
                            st.markdown(f"**Text:** {result.get('text', 'No text found')[:500]}...")
                    time.sleep(1)  # Brief pause for UI flow
                    
            # Step 2: Extract lead information
            with tabs[1]:
                with st.spinner("🧠 Extracting lead information using AI..."):
                    leads = lead_generator.extract_lead_info(search_results)
                    
                    # Filter by minimum score
                    if leads:
                        filtered_leads = [lead for lead in leads if int(float(lead.get('lead_score', 0))) >= min_score]
                        st.session_state.leads = filtered_leads
                        
                        if not filtered_leads:
                            st.warning("⚠️ Found leads, but none met the minimum score criteria.")
                            st.stop()
                    else:
                        st.warning("⚠️ No potential leads were identified in the discussions.")
                        st.stop()
                        
                    st.success(f"✅ Extracted {len(filtered_leads)} potential leads")
                    
                    # Preview the leads
                    if filtered_leads:
                        preview_df = pd.DataFrame(filtered_leads)[['name', 'title', 'company', 'lead_score', 'source']].head(3)
                        st.subheader("Lead Preview:")
                        st.dataframe(preview_df)
                    time.sleep(1)  # Brief pause for UI flow
                    
            # Step 3: Save to Google Sheets
            with tabs[2]:
                with st.spinner("💾 Saving leads to Google Sheets..."):
                    saved_count = lead_generator.save_leads_to_sheet(st.session_state.leads)
                    st.session_state.saved_count = saved_count
                    st.session_state.search_performed = True
                    
                    st.success(f"✅ Successfully saved {saved_count} new leads to Google Sheets")
                    
                    # Add a link to the Google Sheet
                    sheet_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}"
                    st.markdown(f"📊 [Open Google Sheet]({sheet_url})")

    # Display results if available
    if st.session_state.search_performed:
        st.header("📋 Lead Generation Results")
        
        # Success message
        st.markdown(f"""
        <div class="success-message">
            <h3>✅ Lead Generation Complete!</h3>
            <p>Successfully extracted {len(st.session_state.leads)} leads and saved {st.session_state.saved_count} new leads to your Google Sheet.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Organize results in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display the leads in a table
            st.subheader("📊 Extracted Leads")
            if st.session_state.leads:
                leads_df = pd.DataFrame(st.session_state.leads)
                # Reorder and select columns for display
                display_columns = ['name', 'title', 'company', 'email', 'phone', 
                                 'industry', 'lead_score', 'source']
                display_df = leads_df[display_columns] if all(col in leads_df.columns for col in display_columns) else leads_df
                st.dataframe(display_df, use_container_width=True)
                
                # Download option
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Leads as CSV",
                    data=csv,
                    file_name="generated_leads.csv",
                    mime="text/csv",
                )
        
        with col2:
            # Summary statistics
            st.subheader("📈 Summary")
            
            if st.session_state.leads:
                # Source distribution
                st.markdown("**Sources:**")
                source_counts = pd.DataFrame(st.session_state.leads).get('source', pd.Series()).value_counts()
                st.bar_chart(source_counts)
                
                # Lead scores distribution
                st.markdown("**Lead Scores:**")
                score_counts = pd.DataFrame(st.session_state.leads).get('lead_score', pd.Series()).value_counts().sort_index()
                st.bar_chart(score_counts)

    # Display instructions for first-time users
    if not st.session_state.search_performed:
        with st.expander("📚 How to use this tool", expanded=True):
            st.markdown("""
            ### AI Lead Generation Agent Instructions
            
            This tool helps you find potential clients by analyzing online discussions. Here's how to use it:
            
            1. **Enter keywords** in the sidebar to search for potential clients.
               - Use specific phrases people might use when looking for your services
               - Examples: "looking for marketing agency", "need help with web development"
               
            2. **Select sources** where you want to search for discussions.
               - Different platforms have different audiences
               - Try multiple searches with different source combinations
            
            3. **Adjust advanced options** if needed:
               - Maximum results: Controls how many discussions to analyze
               - Minimum lead score: Filters leads by AI-determined quality
            
            4. **Click "Generate Leads"** to start the process.
            
            5. **Review and download** the generated leads or view them in Google Sheets.
            
            ### First Time Setup
            
            Before using this tool, make sure you have:
            
            1. Created a `credentials.json` file with Google Sheets API access
            2. Set up a Google Sheet with the correct sheet name
            3. Configured your Ollama model and environment variables
            
            [View detailed setup instructions](https://github.com/yourusername/lead-generation-agent)
            """)
else:
    # Configuration troubleshooting UI
    st.header("⚙️ Configuration Troubleshooting")
    
    st.markdown("""
    ### Common issues and solutions:
    
    1. **Google Sheets Authentication**
       - Make sure your `credentials.json` file exists and has the correct permissions
       - Verify the path in `GOOGLE_APPLICATION_CREDENTIALS` is correct
       - Ensure the service account has access to the Google Sheet
    
    2. **Google Sheet Access**
       - Check if the Google Sheet ID is correct
       - Verify that the sheet name exists or can be created
       - Make sure your service account has edit access to the sheet
    
    3. **Ollama Configuration**
       - Verify Ollama is running at the configured URL
       - Check if the model is available on your Ollama instance
    
    4. **API Keys**
       - Ensure your Firecrawl API key is valid
    """)
    
    # Environment variable inspection
    with st.expander("Environment Variables Check"):
        # Check essential environment variables
        env_vars = {
            "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY", "Not set"),
            "GOOGLE_SHEET_ID": os.getenv("GOOGLE_SHEET_ID", "Not set"),
            "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "Not set"),
            "OLLAMA_URL": os.getenv("OLLAMA_URL", "Not set"),
            "MODEL_NAME": os.getenv("MODEL_NAME", "Not set"),
            "SHEET_NAME": os.getenv("SHEET_NAME", "Not set")
        }
        
        for var, value in env_vars.items():
            # Mask API keys for security
            if "API_KEY" in var and value != "Not set":
                display_value = value[:5] + "..." + value[-5:] if len(value) > 10 else "***"
            else:
                display_value = value
                
            status = "✅" if value != "Not set" else "❌"
            st.markdown(f"**{var}**: {status} {display_value}")
            
        # Check if credentials file exists
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        if os.path.exists(creds_path):
            st.markdown(f"**Credentials file**: ✅ Found at {creds_path}")
        else:
            st.markdown(f"**Credentials file**: ❌ Not found at {creds_path}")

# Footer section
st.markdown("---")
st.markdown("Powered by Firecrawl API + Ollama + Google Sheets | © 2025")