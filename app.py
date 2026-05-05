"""
Streamlit Dashboard — Salesforce Data AI Pipeline
Run with: streamlit run app.py
"""
import streamlit as st
from sf_connector import SFConnector
from ai_analyzer import AIAnalyzer

st.set_page_config(
    page_title="SF Data AI Pipeline",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Salesforce Data AI Pipeline")
st.caption("AI-powered insights from your live CRM data | Cost: $0")

# Session state
if "connected" not in st.session_state:
    st.session_state.connected = False

# Sidebar — Connect button
with st.sidebar:
    st.header("Connection")
    if st.button("🔌 Connect to Salesforce", use_container_width=True):
        with st.spinner("Authenticating via OAuth..."):
            try:
                st.session_state.sf = SFConnector()
                st.session_state.ai = AIAnalyzer()
                st.session_state.data = st.session_state.sf.get_org_summary()
                st.session_state.connected = True
                st.success("Connected!")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")

    st.divider()
    st.header("About")
    st.markdown("""
    **How it works:**
    1. Connect to your Salesforce org via REST API
    2. Pull Accounts, Opportunities, Cases via SOQL
    3. AI analyzes your data using Groq
    4. Get actionable insights instantly

    **Tech Stack:**
    - simple-salesforce (REST API)
    - LangChain + Groq (AI)
    - Pandas (data processing)
    - Streamlit (dashboard)

    **Cost: $0**
    """)
    st.divider()
    st.caption("Built by Ashish Ghaytadak")
    st.caption("SF Certified PD1 | Agentforce Specialist")

# Main content
if st.session_state.connected:
    data = st.session_state.data
    ai = st.session_state.ai
    stats = data["stats"]

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accounts", stats["total_accounts"])
    c2.metric("Pipeline", f"${stats['total_pipeline']:,.0f}")
    c3.metric("Open Cases", stats["open_cases"])
    c4.metric("High Priority", stats["high_priority_cases"])

    st.divider()

    # Executive Summary
    st.subheader("🧠 AI Executive Summary")
    with st.spinner("Generating executive summary..."):
        summary = ai.generate_executive_summary(stats)
    st.info(summary)

    st.divider()

    # Three tabs for detailed analysis
    tab1, tab2, tab3 = st.tabs([
        "💰 Pipeline Analysis",
        "🏢 Account Health",
        "🎫 Case Trends"
    ])

    with tab1:
        st.subheader("Opportunity Pipeline")
        st.dataframe(data["opportunities"], use_container_width=True)
        if st.button("🤖 Analyze Pipeline with AI", key="pipeline"):
            with st.spinner("AI analyzing pipeline risks..."):
                analysis = ai.analyze_pipeline(data["opportunities"])
            st.markdown(analysis)

    with tab2:
        st.subheader("Account Portfolio")
        st.dataframe(data["accounts"], use_container_width=True)
        if st.button("🤖 Analyze Accounts with AI", key="accounts"):
            with st.spinner("AI scoring account health..."):
                analysis = ai.analyze_accounts(data["accounts"])
            st.markdown(analysis)

    with tab3:
        st.subheader("Support Cases")
        st.dataframe(data["cases"], use_container_width=True)
        if st.button("🤖 Analyze Cases with AI", key="cases"):
            with st.spinner("AI identifying case trends..."):
                analysis = ai.analyze_cases(data["cases"])
            st.markdown(analysis)

else:
    st.info("👈 Click Connect to Salesforce in the sidebar to begin.")
    st.markdown("""
    ### What this app does:
    1. **Connects** to your live Salesforce org
    2. **Pulls** Accounts, Opportunities, and Cases data
    3. **Analyzes** your data with AI (Groq)
    4. **Generates** pipeline risk scores, account health, and case trend insights
    """)
