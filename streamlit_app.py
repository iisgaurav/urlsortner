"""
Professional Streamlit UI for URL Shortener
Clean, modern interface with minimal design.
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
import qrcode
from io import BytesIO

import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="URL Shortener",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Ensure all text is visible */
    body, p, span, label, div {
        color: #2d3748 !important;
    }
    
    h1 {
        color: #1a202c !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2, h3, h4 {
        color: #2d3748 !important;
        font-weight: 600;
    }
    
    /* Labels and text */
    label {
        color: #2d3748 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3182ce;
        color: white !important;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #2c5282;
        box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
    }
    
    /* Input styling */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stDateInput>div>div>input,
    .stTimeInput>div>div>input {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.75rem;
        color: #2d3748 !important;
        background-color: white;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #3182ce;
        box-shadow: 0 0 0 1px #3182ce;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        color: #2d3748 !important;
    }
    
    .stCheckbox label {
        color: #2d3748 !important;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        color: #2d3748;
    }
    
    .success-banner {
        background: #3182ce;
        color: white !important;
        padding: 2rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: white;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: transparent;
        color: #718096 !important;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #3182ce !important;
        border-bottom: 3px solid #3182ce;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #2d3748;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
    }
    
    code {
        color: #2d3748 !important;
    }
    
    /* Links */
    a {
        color: #3182ce !important;
        text-decoration: none;
    }
    
    a:hover {
        color: #2c5282 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'shortened_urls' not in st.session_state:
    st.session_state.shortened_urls = []
if 'show_qr' not in st.session_state:
    st.session_state.show_qr = {}

def generate_qr_code(url):
    """Generate QR code for URL."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2d3748", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def create_short_url(original_url, custom_code=None, expiry_date=None):
    """Create a shortened URL via API."""
    url = f"{API_BASE_URL}/api/shorten/"
    data = {"original_url": original_url}
    
    if custom_code:
        data["custom_code"] = custom_code
    if expiry_date:
        data["expiry_date"] = expiry_date.isoformat()
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json(), None
        else:
            return None, response.json().get('error', 'Unknown error')
    except Exception as e:
        return None, str(e)

def get_analytics(short_code):
    """Get analytics for a shortened URL."""
    url = f"{API_BASE_URL}/api/analytics/{short_code}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, "URL not found"
    except Exception as e:
        return None, str(e)

# Header
st.title("URL Shortener")
st.markdown("Transform long URLs into short, trackable links")

# Sidebar
with st.sidebar:
    st.markdown("<h3 style='color: white;'>Dashboard</h3>", unsafe_allow_html=True)
    
    if st.session_state.shortened_urls:
        total_urls = len(st.session_state.shortened_urls)
        total_clicks = sum([url.get('total_clicks', 0) for url in st.session_state.shortened_urls])
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 16px; border-radius: 8px; margin: 12px 0;'>
                <h2 style='color: white; margin: 0; font-size: 32px;'>{total_urls}</h2>
                <p style='color: rgba(255,255,255,0.8); margin: 4px 0 0 0; font-size: 14px;'>Total URLs</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 16px; border-radius: 8px; margin: 12px 0;'>
                <h2 style='color: white; margin: 0; font-size: 32px;'>{total_clicks}</h2>
                <p style='color: rgba(255,255,255,0.8); margin: 4px 0 0 0; font-size: 14px;'>Total Clicks</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No URLs created yet")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Refresh Data"):
        st.rerun()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Create URL", "Analytics", "History", "Insights"])

# Tab 1: Create URL
with tab1:
    st.subheader("Create New Short URL")
    
    original_url = st.text_input(
        "Enter URL",
        placeholder="https://example.com/your/long/url",
        help="Paste the URL you want to shorten"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        use_custom = st.checkbox("Use custom code")
        if use_custom:
            custom_code = st.text_input("Custom code", placeholder="mylink")
        else:
            custom_code = None
    
    with col2:
        use_expiry = st.checkbox("Set expiry date")
        if use_expiry:
            expiry_date = st.date_input("Expiry date")
            expiry_time = st.time_input("Expiry time")
            expiry_datetime = datetime.combine(expiry_date, expiry_time)
        else:
            expiry_datetime = None
    
    if st.button("Create Short URL", type="primary"):
        if not original_url:
            st.error("Please enter a URL")
        elif not original_url.startswith(('http://', 'https://')):
            st.error("URL must start with http:// or https://")
        else:
            with st.spinner("Creating..."):
                result, error = create_short_url(original_url, custom_code, expiry_datetime)
                
                if result:
                    short_code = result['short_url'].split('/')[-1]
                    
                    st.markdown(f"""
                        <div class="success-banner">
                            <h3 style='color: white; margin-top: 0;'>Short URL Created</h3>
                            <h2 style='color: white; margin: 8px 0;'>{result['short_url']}</h2>
                            <p style='color: rgba(255,255,255,0.9); margin: 0;'>
                                Original: {result['original_url'][:60]}...
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.code(result['short_url'], language=None)
                    
                    with col2:
                        qr_buffer = generate_qr_code(result['short_url'])
                        st.download_button(
                            label="Download QR Code",
                            data=qr_buffer,
                            file_name=f"qr_{short_code}.png",
                            mime="image/png"
                        )
                    
                    # Show QR code
                    st.image(generate_qr_code(result['short_url']), width=200)
                    
                    # Add to history
                    st.session_state.shortened_urls.insert(0, {
                        'short_url': result['short_url'],
                        'original_url': result['original_url'],
                        'created_at': result['created_at'],
                        'short_code': short_code,
                        'total_clicks': 0
                    })
                else:
                    st.error(f"Error: {error}")

# Tab 2: Analytics
with tab2:
    st.subheader("URL Analytics")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        short_code_input = st.text_input("Short code", placeholder="abc123")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("Get Analytics", type="primary")
    
    if analyze_btn and short_code_input:
        with st.spinner("Loading..."):
            analytics, error = get_analytics(short_code_input)
            
            if analytics:
                st.success("Analytics loaded")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Clicks", analytics['total_clicks'])
                
                with col2:
                    status_text = "Active" if analytics['is_active'] else "Expired"
                    st.metric("Status", status_text)
                
                with col3:
                    created = datetime.fromisoformat(analytics['created_at'].replace('Z', '+00:00'))
                    st.metric("Created", created.strftime("%b %d, %Y"))
                
                with col4:
                    if analytics.get('expiry_date'):
                        expiry = datetime.fromisoformat(analytics['expiry_date'].replace('Z', '+00:00'))
                        st.metric("Expires", expiry.strftime("%b %d, %Y"))
                    else:
                        st.metric("Expires", "Never")
                
                # URL Info
                st.markdown(f"""
                    <div class="info-card">
                        <h4>URL Information</h4>
                        <p><strong>Short Code:</strong> {analytics['short_code']}</p>
                        <p><strong>Original URL:</strong> {analytics['original_url']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Recent Clicks
                if analytics.get('recent_clicks'):
                    st.markdown("### Recent Activity")
                    
                    clicks_df = pd.DataFrame(analytics['recent_clicks'])
                    clicks_df['timestamp'] = pd.to_datetime(clicks_df['timestamp'])
                    
                    # Timeline chart
                    fig = px.scatter(clicks_df, x='timestamp', y=[1]*len(clicks_df),
                                   hover_data=['ip_address'],
                                   title="Click Timeline")
                    fig.update_traces(marker=dict(size=12, color='#3182ce'))
                    fig.update_yaxes(showticklabels=False)
                    fig.update_layout(height=200, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(
                        clicks_df[['timestamp', 'ip_address']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No clicks recorded yet")
            else:
                st.error(f"Error: {error}")

# Tab 3: History
with tab3:
    st.subheader("URL History")
    
    if st.session_state.shortened_urls:
        for idx, url_data in enumerate(st.session_state.shortened_urls):
            with st.container():
                st.markdown(f"""
                    <div class="info-card">
                        <h4>{url_data['short_url']}</h4>
                        <p><strong>Original:</strong> {url_data['original_url'][:80]}...</p>
                        <p style='color: #718096; font-size: 0.875rem;'>Created: {url_data['created_at']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.code(url_data['short_url'], language=None)
                
                with col2:
                    if st.button("View Stats", key=f"stats_{idx}"):
                        analytics, _ = get_analytics(url_data['short_code'])
                        if analytics:
                            st.session_state.shortened_urls[idx]['total_clicks'] = analytics['total_clicks']
                            st.success(f"{analytics['total_clicks']} clicks")
                            st.rerun()
                
                with col3:
                    if st.button("Show QR", key=f"qr_btn_{idx}"):
                        st.session_state.show_qr[idx] = not st.session_state.show_qr.get(idx, False)
                        st.rerun()
                
                if st.session_state.show_qr.get(idx, False):
                    st.image(generate_qr_code(url_data['short_url']), width=200)
    else:
        st.info("No URLs created yet. Go to 'Create URL' tab to get started.")

# Tab 4: Insights
with tab4:
    st.subheader("Analytics Insights")
    
    if st.session_state.shortened_urls and len(st.session_state.shortened_urls) > 0:
        df = pd.DataFrame(st.session_state.shortened_urls)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top URLs by Clicks")
            top_urls = df.nlargest(5, 'total_clicks')[['short_code', 'total_clicks']]
            
            fig = px.bar(top_urls, x='short_code', y='total_clicks',
                        color_discrete_sequence=['#3182ce'])
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Click Distribution")
            
            fig = go.Figure(data=[go.Pie(
                labels=df['short_code'],
                values=df['total_clicks'],
                hole=0.4,
                marker=dict(colors=['#3182ce', '#4299e1', '#63b3ed', '#90cdf4'])
            )])
            fig.update_layout(height=300, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary stats
        st.markdown("#### Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Highest Clicks", f"{df['total_clicks'].max()}")
        with col2:
            st.metric("Average Clicks", f"{df['total_clicks'].mean():.1f}")
        with col3:
            st.metric("Total URLs", len(df))
    else:
        st.info("Create URLs to see insights")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 8px; border: 1px solid #e2e8f0;'>
        <p style='color: #718096; margin: 0;'>
            Django REST API • Redis • PostgreSQL • Streamlit
        </p>
    </div>
""", unsafe_allow_html=True)
