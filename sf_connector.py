"""
Salesforce Data Connector
Authenticates via OAuth and pulls Accounts, Opportunities, Cases via SOQL
"""
from simple_salesforce import Salesforce
import pandas as pd
from config import Config


class SFConnector:
    """Connects to Salesforce and extracts CRM data."""

    def __init__(self):
        """Authenticate to Salesforce."""
        print("Connecting to Salesforce...")
        self.sf = Salesforce(
            username=Config.SF_USERNAME,
            password=Config.SF_PASSWORD,
            security_token=Config.SF_SECURITY_TOKEN,
            domain=Config.SF_DOMAIN
        )
        print(f"  Connected: {self.sf.sf_instance}")

    def _query_to_df(self, query: str) -> pd.DataFrame:
        """Execute SOQL query and return as DataFrame."""
        result = self.sf.query(query)
        records = result.get("records", [])
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        # Remove Salesforce metadata column
        if "attributes" in df.columns:
            df = df.drop(columns=["attributes"])
        return df

    def get_accounts(self, limit: int = 50) -> pd.DataFrame:
        """Pull Account data."""
        print(f"  Querying Accounts (limit={limit})...")
        query = f"""
            SELECT Id, Name, Industry, AnnualRevenue,
                   NumberOfEmployees, Rating, Type,
                   BillingState, CreatedDate
            FROM Account
            ORDER BY CreatedDate DESC
            LIMIT {limit}
        """
        df = self._query_to_df(query)
        print(f"  Retrieved {len(df)} accounts")
        return df

    def get_opportunities(self, limit: int = 100) -> pd.DataFrame:
        """Pull Opportunity data."""
        print(f"  Querying Opportunities (limit={limit})...")
        query = f"""
            SELECT Id, Name, StageName, Amount,
                   Probability, CloseDate, Type, LeadSource
            FROM Opportunity
            ORDER BY CreatedDate DESC
            LIMIT {limit}
        """
        df = self._query_to_df(query)
        print(f"  Retrieved {len(df)} opportunities")
        return df

    def get_cases(self, limit: int = 100) -> pd.DataFrame:
        """Pull Case data."""
        print(f"  Querying Cases (limit={limit})...")
        query = f"""
            SELECT Id, Subject, Status, Priority,
                   Type, Origin, CreatedDate
            FROM Case
            ORDER BY CreatedDate DESC
            LIMIT {limit}
        """
        df = self._query_to_df(query)
        print(f"  Retrieved {len(df)} cases")
        return df

    def get_org_summary(self) -> dict:
        """Pull all data and compute summary stats."""
        accounts = self.get_accounts()
        opportunities = self.get_opportunities()
        cases = self.get_cases()

        # Compute stats safely
        total_pipeline = 0
        if "Amount" in opportunities.columns:
            total_pipeline = pd.to_numeric(
                opportunities["Amount"], errors="coerce"
            ).sum()

        high_priority = 0
        if "Priority" in cases.columns:
            high_priority = len(cases[cases["Priority"] == "High"])

        open_cases = 0
        if "Status" in cases.columns:
            open_cases = len(cases[cases["Status"] != "Closed"])

        return {
            "accounts": accounts,
            "opportunities": opportunities,
            "cases": cases,
            "stats": {
                "total_accounts": len(accounts),
                "total_opportunities": len(opportunities),
                "total_pipeline": total_pipeline,
                "total_cases": len(cases),
                "open_cases": open_cases,
                "high_priority_cases": high_priority,
            }
        }


# Quick test
if __name__ == "__main__":
    connector = SFConnector()
    data = connector.get_org_summary()
    print("\nORG SUMMARY:")
    for key, val in data["stats"].items():
        print(f"  {key}: {val}")
