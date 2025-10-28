import requests
import pandas as pd
import datetime
import re

def fetch_previous_day_amfi_nav():
    url = "https://www.amfiindia.com/spages/NAVAll.txt"
    print("📥 Fetching latest AMFI NAV data...")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("❌ Failed to fetch data. Status:", response.status_code)
            return

        text = response.text.strip()
        if len(text) < 1000:
            print("⚠️ AMFI data seems empty. Try again later.")
            return

        date_match = re.search(r"\d{2}-[A-Za-z]{3}-\d{4}", text)
        if date_match:
            data_date = datetime.datetime.strptime(date_match.group(), "%d-%b-%Y").date()
        else:
            data_date = datetime.date.today() - datetime.timedelta(days=1)

        filename = f"data/AMFI_NAV_{data_date}.csv"
        with open(f"{filename}", "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Saved NAV data for {data_date} → {filename}")

        # Optional: Convert to DataFrame for your recommender later
        df = pd.read_csv(f"{filename}", sep=';', on_bad_lines='skip', encoding='utf-8')
        print(f"📊 Loaded {len(df)} valid rows from {filename}")
        return df

    except Exception as e:
        print("❌ Error:", e)

# Run
fetch_previous_day_amfi_nav()
