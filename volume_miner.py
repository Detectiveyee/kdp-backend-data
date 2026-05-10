import requests
import string
import time
import pandas as pd
from datetime import datetime
import os

# The highly targeted Seed Niches
SEED_KEYWORDS = [
    "gay shifter ", 
    "mm omegaverse ", 
    "gay viking ", 
    "orc captive mm ",
    "gay monster romance ",
    "mm paranormal "
]

def get_amazon_suggestions(query):
    # Amazon's hidden autocomplete API for Books
    url = f"https://completion.amazon.com/api/2017/suggestions?page-type=Search&lop=en_US&site-variant=desktop&client-info=amazon-search-ui&mid=ATVPDKIKX0DER&alias=stripbooks&prefix={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        return [item['value'] for item in data.get('suggestions', [])]
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def run_volume_miner():
    all_data = []
    alphabet = list(string.ascii_lowercase) # a, b, c, d...
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    for seed in SEED_KEYWORDS:
        print(f"Mining Search Volume for: '{seed}'...")
        
        # 1. Check the seed word itself
        base_results = get_amazon_suggestions(seed.strip())
        for rank, res in enumerate(base_results, start=1):
            all_data.append({
                "Date_Checked": today_date,
                "Seed_Keyword": seed.strip(),
                "Long_Tail_Keyword": res,
                "Autocomplete_Rank": rank # 1 is highest volume, 10 is lowest
            })
        
        # 2. The Alphabet Soup (seed + a, seed + b, etc.)
        for letter in alphabet:
            search_term = seed + letter
            suggestions = get_amazon_suggestions(search_term)
            
            for rank, res in enumerate(suggestions, start=1):
                all_data.append({
                    "Date_Checked": today_date,
                    "Seed_Keyword": seed.strip(),
                    "Long_Tail_Keyword": res,
                    "Autocomplete_Rank": rank
                })
            
            time.sleep(1) # Polite delay
            
    # Save to CSV for the Chrome Extension to read
    df = pd.DataFrame(all_data).drop_duplicates(subset=['Long_Tail_Keyword'])
    df.to_csv('search_volume_db.csv', index=False)
    print(f"SUCCESS: Saved {len(df)} keywords to the database.")

if __name__ == "__main__":
    run_volume_miner()
