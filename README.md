# $\text{FundFocus}$ AI: Personalized Mutual Fund Dashboard 📈🧠

**$\text{FundFocus}$ AI** is a modern, AI-driven financial dashboard designed to cut through the complexity of mutual fund investing. It provides users with a **personalized, data-backed analysis** of funds based on their unique risk appetite and current market sentiment.

Forget generic star ratings. $\text{FundFocus}$ AI offers **actionable intelligence** by combining classical financial metrics with cutting-edge Machine Learning and Natural Language Processing ($\text{NLP}$).

## ✨ Features

### 1. Personalized Risk Scoring & Recommendations

* **User Risk Input:** Users answer a brief questionnaire to define their **Risk Appetite **.
* **Propensity Model (ML):** The system uses a trained $\text{Scikit-learn}$ classification model to score the **suitability** of every selected fund against the user's $\text{Risk\_Score}$.
* **Actionable Insights:** Provides a clear recommendation on **fund suitability** (e.g., "Highly Suitable for your Moderate Risk Profile").

### 2. Comprehensive Financial Analysis

* **Fund Performance Metrics:** Fetches and displays core financial data including:
    * Annualized Returns (1Y, 3Y, 5Y)
    * Annualized Volatility ($\text{Std. Dev}$)
    * $\text{Sharpe Ratio}$
    * $\text{Max Drawdown}$
    * Expense Ratio
* **Comparative Analysis:** Visual comparison of selected funds across key metrics (returns vs. risk) using interactive charts ($\text{Chart.js}$ / $\text{D3.js}$).

### 3. AI-Powered Sentiment Cards (NLP)

* **Real-time News Fetching:** Uses $\text{NewsAPI}$ to retrieve relevant financial headlines related to the fund's sector (e.g., Banking, Pharma, $\text{IT}$).
* **FinBERT Sentiment Analysis:** A $\text{Hugging Face Transformers}$ model ($\text{FinBERT}$) processes the headlines to determine the overall market sentiment ($\text{Positive}$, $\text{Neutral}$, or $\text{Negative}$).
* **Contextual Insight:** Displays $\text{AI-Powered Sentiment Cards}$ with a summary like, *"Positive market sentiment on banking funds due to $\text{RBI}$ rate cuts,"* providing context beyond raw numbers.

## 🛠️ Technology Stack

This project utilizes a modern, robust, and scalable microservice architecture.

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | $\text{React.js}$ | Interactive user interface and data visualization. |
| | $\text{Chart.js}$ / $\text{D3.js}$ | Rendering dynamic fund performance charts. |
| | $\text{Tailwind CSS}$ | Utility-first $\text{CSS}$ framework for rapid, responsive styling. |
| **Backend / API** | $\text{FastAPI}$ (Python) | Lightweight, high-performance web framework for serving data and $\text{ML}$ predictions. |
| **Database** | $\text{PostgreSQL}$ | Stores historical fund data, $\text{ML}$ model predictions, and user risk profiles. |
| **AI / ML** | $\text{Scikit-learn}$ | Training and deployment of the **Risk Propensity Model**. |
| | $\text{Hugging Face Transformers}$ ($\text{FinBERT}$) | Implementing sector-specific **Sentiment Analysis**. |
| **Data Sources** | $\text{mftool}$ | Primary source for Indian Mutual Fund $\text{NAV}$ history and scheme details. |
| | $\text{NewsAPI}$ | Source for global and regional financial news headlines. |
| **DevOps** | $\text{Docker}$ | Containerization for consistent and isolated development/deployment environments. |
| | $\text{Coursera Devbox}$ | The primary development environment used for local setup and rapid iteration. |

## 🚀 Getting Started

### Prerequisites

1.  Python 3.9+
2.  $\text{Node.js}$ / $\text{npm}$ (for $\text{React}$ frontend)
3.  $\text{Docker}$ (recommended for deployment)

### Local Setup (Using Coursera Devbox or Local Environment)

```bash
# 1. Clone the Repository:
git clone [https://github.com/yourusername/fundfocus-ai.git](https://github.com/yourusername/fundfocus-ai.git)
cd fundfocus-ai

# 2. Set up the Backend (FastAPI & ML):
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate 

# Install dependencies
pip install -r requirements.txt 

# ⚠️ Environment Variables: Set your NewsAPI key and PostgreSQL connection string
# export NEWS_API_KEY='YOUR_KEY' 

# Run the ML model training script once (to train the initial Propensity Model)
python ml_train.py 

# Start the FastAPI server
uvicorn app.main:app --reload

# 3. Set up the Frontend (React):
cd frontend
npm install

# Start the React development server
npm start
