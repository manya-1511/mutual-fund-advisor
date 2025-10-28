import pandas as pd
import numpy as np
import re

# ----------------------------
# 1️⃣ Clean & Parse Fund Data
# ----------------------------
def clean_amfi_data(df):
    print("🧹 Cleaning and parsing AMFI data...")

    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(how='all')

    # Drop duplicates & handle missing NAVs
    df = df.drop_duplicates(subset=['Scheme Name'], keep='last')
    df = df.dropna(subset=['Net Asset Value', 'Scheme Name'])
    df['Net Asset Value'] = pd.to_numeric(df['Net Asset Value'], errors='coerce')
    df = df.dropna(subset=['Net Asset Value'])

    # Detect fund category
    def detect_category(name):
        name = name.lower()
        if any(word in name for word in ['equity', 'large cap', 'midcap', 'small cap', 'elss']):
            return 'Equity'
        elif any(word in name for word in ['debt', 'bond', 'income', 'gilt', 'liquid']):
            return 'Debt'
        elif any(word in name for word in ['hybrid', 'balanced', 'aggressive']):
            return 'Hybrid'
        else:
            return 'Other'

    df['Category'] = df['Scheme Name'].apply(detect_category)
    df['Scheme Name'] = df['Scheme Name'].str.strip().str.replace(r'\s+', ' ', regex=True)

    # Simulated return data (in %)
    np.random.seed(42)
    df['1D Return (%)'] = np.random.uniform(-1, 1, len(df)).round(2)
    df['1W Return (%)'] = np.random.uniform(-3, 3, len(df)).round(2)
    df['1M Return (%)'] = np.random.uniform(-8, 8, len(df)).round(2)
    df['6M Return (%)'] = np.random.uniform(-15, 20, len(df)).round(2)
    df['1Y Return (%)'] = np.random.uniform(-25, 30, len(df)).round(2)
    df['3Y Return (%)'] = np.random.uniform(-40, 60, len(df)).round(2)
    df['Volatility'] = np.random.uniform(1, 5, len(df)).round(2)

    df = df[['Scheme Name', 'Category', 'Net Asset Value',
             '1D Return (%)', '1W Return (%)', '1M Return (%)',
             '6M Return (%)', '1Y Return (%)', '3Y Return (%)', 'Volatility']]

    print(f"✅ Cleaned {len(df)} entries successfully.")
    return df


# ---------------------------------------
# 2️⃣ Take User Investment Profile Inputs
# ---------------------------------------
def get_user_profile():
    print("\n🧍 Enter your investment profile:\n")

    user = {
        "FundType": input("Type of Mutual Fund (Equity / Debt / Hybrid / Any): ").capitalize(),
        "Risk": input("Risk Tolerance (Low / Medium / High): ").capitalize(),
        "Horizon": input("Investment Horizon (Short / Long): ").capitalize(),
        "Goal": input("Financial Goal (Growth / Income / Balanced): ").capitalize(),
        "Knowledge": input("Investment Knowledge (Beginner / Intermediate / Expert): ").capitalize(),
        "AgeIncome": input("Age Group / Income Level (e.g., <25 Low / 25-40 Medium / >40 High): ").capitalize()
    }

    print("\n✅ Profile recorded successfully!\n")
    return user


# ------------------------------------------------
# 3️⃣ Recommend Funds Based on User Profile & Data
# ------------------------------------------------
def recommend_funds(df, user):
    print("🤖 Generating personalized fund recommendations...")

    # Suitability mapping logic
    category_map = {
        "Low": ["Debt"],
        "Medium": ["Hybrid", "Debt"],
        "High": ["Equity", "Hybrid"]
    }

    goal_map = {
        "Growth": ["Equity"],
        "Income": ["Debt"],
        "Balanced": ["Hybrid"]
    }

    # Merge risk + goal + selected fund type filters
    suitable_categories = set(category_map.get(user["Risk"], [])) | set(goal_map.get(user["Goal"], []))

    if user["FundType"] != "Any":
        suitable_categories = suitable_categories & {user["FundType"]}

    filtered_df = df[df["Category"].isin(suitable_categories)]

    if filtered_df.empty:
        print("⚠️ No funds match your preferences. Try changing your inputs.")
        return pd.DataFrame()

    # Compute Adjusted Score (weighted returns - volatility)
    filtered_df['Adjusted Score'] = (
        0.4 * filtered_df['3Y Return (%)'] +
        0.2 * filtered_df['1Y Return (%)'] +
        0.15 * filtered_df['6M Return (%)'] +
        0.1 * filtered_df['1M Return (%)'] +
        0.1 * filtered_df['1W Return (%)'] +
        0.05 * filtered_df['1D Return (%)'] -
        0.5 * filtered_df['Volatility']
    )

    top_funds = filtered_df.sort_values(by='Adjusted Score', ascending=False).head(10)

    print(f"\n📈 Top 10 Recommended {user['FundType']} Funds for {user['Risk']} Risk and {user['Goal']} Goal:\n")
    print(top_funds[['Scheme Name', 'Category', 'Net Asset Value',
                     '6M Return (%)', '1Y Return (%)', '3Y Return (%)',
                     'Volatility', 'Adjusted Score']])

    top_funds.to_csv("data/recommended_funds.csv", index=False)
    print("\n💾 Recommendations saved to data/recommended_funds.csv")

    return top_funds


# ------------------------------------------------
# 4️⃣ Model Explanation (Current Logic)
# ------------------------------------------------
def explain_model():
    print("\n🧠 Model Used: Rule-Based Hybrid Scoring System\n")
    print("""
🔹 **Model Type:** Rule-Based + Weighted Scoring (Heuristic AI)
🔹 **Scoring Formula:**
     Adjusted Score = 0.4*(3Y Return) + 0.2*(1Y Return) + 0.15*(6M Return)
                     + 0.1*(1M Return) + 0.1*(1W Return) + 0.05*(1D Return)
                     - 0.5*(Volatility)

🔹 **Purpose:** Simulates analyst-style evaluation of long-term vs. short-term performance.
🔹 **Next Step:** Replace with ML model trained on user preferences and market data
    (e.g., KNN / Random Forest / Neural Network Recommender).
    """)


# -----------------------
# 🧠 Example Full Workflow
# -----------------------
if __name__ == "__main__":
    # Load previous AMFI data (from your existing script)
    df = pd.read_csv("data/AMFI_NAV_2025-10-27.csv", sep=';', on_bad_lines='skip', encoding='utf-8')
    cleaned_df = clean_amfi_data(df)

    user_profile = get_user_profile()
    explain_model()
    recommend_funds(cleaned_df, user_profile)
