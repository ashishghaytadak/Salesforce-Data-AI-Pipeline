# 📊 Salesforce Data AI Pipeline

AI-powered CRM analytics that connects to a live Salesforce org and generates business insights using Google Gemini. 100% free.

## Architecture

```
Salesforce Org → OAuth Authentication → SOQL Queries → Pandas Processing → Gemini AI Analysis → Streamlit Dashboard
```

## Features

- **Live Salesforce connection** via OAuth (simple-salesforce)
- **SOQL data extraction** — Accounts, Opportunities, Cases
- **AI pipeline risk analysis** — identifies at-risk deals with reasons
- **AI account health scoring** — flags accounts needing attention
- **AI case trend identification** — finds bottlenecks and recommends fixes
- **Executive summary generation** — 5-sentence CTO-level overview
- **Interactive dashboard** with metrics, data tables, and AI insights

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Data Source | Live Salesforce Org (REST API + OAuth) | Free |
| Processing | Pandas + SOQL | Free |
| AI Engine | LangChain + Google Gemini Flash | Free |
| Dashboard | Streamlit | Free |
| **Total** | | **$0** |

## Quick Start

```bash
# Clone
git clone https://github.com/ashishghaytadak/salesforce-data-ai-pipeline.git
cd salesforce-data-ai-pipeline

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Salesforce credentials + Gemini API key

# Launch
streamlit run app.py
```

## How to Get Your Salesforce Security Token

1. Log into your Salesforce org
2. Click avatar (top right) → Settings
3. My Personal Information → Reset My Security Token
4. Check your email for the token

## How It Relates to Salesforce Data Cloud & Agentforce

| This Project | Salesforce Equivalent |
|---|---|
| SOQL data extraction | Data Cloud data ingestion |
| Pandas processing | Data Cloud harmonization |
| Gemini AI analysis | Agentforce AI reasoning |
| Streamlit dashboard | CRM Analytics activation |
| Executive summary | Agentforce agent response |

## Screenshots

_Coming soon_

## Author

**Ashish Ghaytadak**
- Salesforce Certified Platform Developer I
- Salesforce Certified Agentforce Specialist
- Salesforce Certified Administrator
- MS in Information Systems, Syracuse University (2026)
