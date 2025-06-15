import os
import requests
import pandas as pd
from functools import lru_cache
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("CH_API_KEY")
BASE_URL = "https://api.company-information.service.gov.uk"

def _get_json(url: str):
    r = requests.get(url, auth=(API_KEY, ""))
    r.raise_for_status()
    return r.json()

@lru_cache(maxsize=128)
def search_companies(term: str) -> pd.DataFrame:
    term = term.replace(" ", "+")
    data = _get_json(f"{BASE_URL}/search?q={term}")
    items = data.get("items", [])
    return pd.DataFrame([
        {
            "Company Name": x["title"],
            "Company Number": x.get("company_number")
        }
        for x in items
    ])

@lru_cache(maxsize=128)
def get_officers(company_number: str) -> pd.DataFrame:
    data = _get_json(f"{BASE_URL}/company/{company_number}/officers")
    return pd.DataFrame([
        {
            "Name": x.get("name"),
            "DOB month": x.get("date_of_birth", {}).get("month"),
            "DOB year": x.get("date_of_birth", {}).get("year")
        }
        for x in data.get("items", [])
    ])

# ------------------ Main CLI logic ------------------

if __name__ == "__main__":
    print("✅ Script started")
    print("🔐 API Key loaded:", "✅" if API_KEY else "❌ None")

    company_term = input("📨 Please enter a company name to search: ")
    results_df = search_companies(company_term)

    if results_df.empty:
        print("❌ No results found.")
        exit()

    print("\n📦 Matching Companies:")
    print(results_df)

    try:
        user_index = int(input("🔢 Enter the index number of the company: "))
        selected_row = results_df.iloc[user_index]
        selected_number = selected_row["Company Number"]
    except (ValueError, IndexError):
        print("❌ Invalid index.")
        exit()

    print(f"\n🔍 Fetching officers for: {selected_row['Company Name']} [{selected_number}]")
    officer_df = get_officers(selected_number)

    print("\n👥 Officers:")
    print(officer_df if not officer_df.empty else "No officer data found.")