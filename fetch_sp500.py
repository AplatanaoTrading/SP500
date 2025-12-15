import pandas as pd
import requests
from io import StringIO

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print("Failed to fetch page")
            return []
            
        html = response.text
        # Use pandas to read the table directly, matching the table id or specific text
        dfs = pd.read_html(StringIO(html), match='Symbol')
        
        if not dfs:
            print("No tables found with 'Symbol' column")
            return []

        # The first table is usually the S&P 500 component list
        sp500_table = dfs[0]
        tickers = sp500_table['Symbol'].tolist()
        
        return tickers
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    if tickers:
        print(f"Found {len(tickers)} tickers.")
        # Save to current directory
        with open('sp.csv', 'w') as f:
            for ticker in tickers:
                f.write(f"{ticker}\n")
        print("Successfully saved to sp.csv")
    else:
        print("No tickers found.")
