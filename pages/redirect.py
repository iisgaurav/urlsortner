# pages/redirect.py
# Streamlit page to handle redirects

import streamlit as st
import requests
import os

st.set_page_config(page_title="Redirecting...", page_icon="🔗")

# Get the query parameters
params = st.query_params

# Check if we have a short code
if "code" in params:
    short_code = params["code"]
   
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    try:
        # Call Django API to get redirect URL
        response = requests.get(f"{API_BASE_URL}/{short_code}/", allow_redirects=False)
        
        if response.status_code == 302:
            target_url = response.headers.get('Location')
            
            # Redirect using HTML meta refresh
            st.markdown(f"""
                <meta http-equiv="refresh" content="0; url={target_url}">
                <script>window.location.href = "{target_url}";</script>
            """, unsafe_allow_html=True)
            
            st.success(f "Redirecting to {target_url}...")
            
        elif response.status_code == 404:
            st.error("Short URL not found!")
        elif response.status_code == 410:
            st.error("This link has expired!")
        else:
            st.error("An error occurred")
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.error("No short code provided")
