import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import time
import re

# 1. Keywords to track for Competition (Total Search Results)
KEYWORDS_TO_TRACK = [
    "gay shifter",
    "mm omegaverse",
    "gay viking captive"
]

# 2. ASINs to track for Daily BSR (The "Time Machine" feature)
ASINS_TO_TRACK = [
    "B0GR8W5PZ2", # Example ASIN - Replace with top competitors
    "B0C9XYZ123" 
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def track_competition():
    print("--- Starting Competition Tracker ---")
    comp_data = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    for kw in KEYWORDS_TO_TRACK:
        url = f"https://www.amazon.com/s?k={kw.replace(' ', '+')}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.content, "html.parser")
            
            # Scrape the "1-16 of over 50,000 results" text
            count_span = soup.find('div', class_='sg-col-inner')
            total_results = "N/A"
            if count_span:
                text = count_span.text.strip()
                if "results for" in text:
                    total_results = text.split('results for')[0].strip()
            
            comp_data.append({
                "Date": today,
                "Keyword": kw,
                "Total_Competition": total_results
            })
            time.sleep(4) # Delay for search pages
        except Exception as e:
            print(f"Error tracking {kw}: {e}")

    df = pd.DataFrame(comp_data)
    file_name = 'competition_db.csv'
    df.to_csv(file_name, mode='a', header=not os.path.exists(file_name), index=False)
    print("Competition database updated.")

def track_bsr():
    print("--- Starting BSR History Tracker ---")
    bsr_data = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    for asin in ASINS_TO_TRACK:
        url = f"https://www.amazon.com/dp/{asin}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.content, "html.parser")
            
            # Extract BSR using Regex (Amazon hides it in various places)
            page_text = soup.get_text()
            bsr_match = re.search(r'#([0-9,]+) in Kindle Store', page_text)
            
            bsr_value = "N/A"
            if bsr_match:
                bsr_value = bsr_match.group(1).replace(',', '')
                
            bsr_data.append({
                "Date": today,
                "ASIN": asin,
                "BSR": bsr_value
            })
            time.sleep(10) # Heavy 10-second delay. Product pages are highly guarded.
        except Exception as e:
            print(f"Error tracking ASIN {asin}: {e}")

    df = pd.DataFrame(bsr_data)
    file_name = 'bsr_history_db.csv'
    df.to_csv(file_name, mode='a', header=not os.path.exists(file_name), index=False)
    print("BSR History database updated.")

if __name__ == "__main__":
    track_competition()
    track_bsr()
