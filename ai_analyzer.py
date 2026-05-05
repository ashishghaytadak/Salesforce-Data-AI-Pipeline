"""
AI Analyzer — LLM-powered CRM insights
Uses Google Gemini (free) to analyze Salesforce data
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from config import Config
import json


class AIAnalyzer:
    """Generates AI insights from Salesforce CRM data."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.2,
            max_output_tokens=2000
        )
        print("  AI Analyzer ready (Gemini free tier)")

    def analyze_pipeline(self, opp_df) -> str:
        """Analyze opportunity pipeline for risks and recommendations."""
        data = opp_df.to_string(index=False, max_rows=25)
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a sales analytics expert reviewing a CRM pipeline. "
             "Provide: 1) Pipeline health score (1-10 with justification), "
             "2) Top 3 deals at risk and why, "
             "3) Three specific actions for the sales team. "
             "Be concise and actionable. Use bullet points."),
            ("human", "Current pipeline data:\n\n{data}")
        ])
        response = self.llm.invoke(prompt.format_messages(data=data))
        return response.content

    def analyze_accounts(self, acc_df) -> str:
        """Analyze account portfolio for health and opportunities."""
        data = acc_df.to_string(index=False, max_rows=25)
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a CRM strategist analyzing an account portfolio. "
             "Provide: 1) Overall account health overview, "
             "2) Top 3 accounts needing immediate attention and why, "
             "3) Cross-sell or upsell opportunities you can identify. "
             "Be specific and data-driven."),
            ("human", "Account data:\n\n{data}")
        ])
        response = self.llm.invoke(prompt.format_messages(data=data))
        return response.content

    def analyze_cases(self, case_df) -> str:
        """Analyze support cases for trends and bottlenecks."""
        data = case_df.to_string(index=False, max_rows=25)
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a service operations analyst reviewing support cases. "
             "Provide: 1) Trend summary by priority and type, "
             "2) Bottleneck identification, "
             "3) Three recommendations to reduce resolution time. "
             "Be concise and actionable."),
            ("human", "Open cases data:\n\n{data}")
        ])
        response = self.llm.invoke(prompt.format_messages(data=data))
        return response.content

    def generate_executive_summary(self, stats: dict) -> str:
        """Generate a concise executive summary from CRM metrics."""
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a CTO advisor. Generate a concise executive summary "
             "(5 sentences max) from these CRM metrics. "
             "Focus on actionable insights, risks, and opportunities."),
            ("human", "CRM Metrics:\n{metrics}")
        ])
        response = self.llm.invoke(prompt.format_messages(metrics=json.dumps(stats, indent=2)))
        return response.content


# Quick test
if __name__ == "__main__":
    from sf_connector import SFConnector
    print("Connecting to Salesforce...")
    sf = SFConnector()
    data = sf.get_org_summary()
    print("\nInitializing AI Analyzer...")
    ai = AIAnalyzer()
    print("\nGenerating Executive Summary...")
    summary = ai.generate_executive_summary(data["stats"])
    print(f"\n{summary}")
