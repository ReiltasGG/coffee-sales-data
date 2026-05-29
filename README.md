# ☕ PulseBoard — Coffee Shop Sales Dashboard

PulseBoard is an interactive business analytics dashboard built with Python, Streamlit, and Plotly. It transforms raw coffee shop sales data into a clean, filterable dashboard that gives store owners and managers real insight into their business performance.

Designed with a custom coffee-themed dark UI — deep espresso backgrounds, caramel accents, and warm cream typography.

## Features
- **KPI Cards** — Total revenue, transactions, avg order value, top location
- **Revenue Over Time** — Monthly trends broken down by store location
- **Revenue by Category** — Which product categories drive the most revenue
- **Busiest Hours** — Peak traffic times per location
- **Top 10 Products** — Best performing individual items by revenue
- **Location Revenue Share** — Donut chart breakdown across all 3 stores
- **Monthly Transaction Volume** — Stacked category breakdown over time
- **Sidebar Filters** — Filter everything by location, category, and date range

## Tech Stack
| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data processing | Pandas |
| Dashboard framework | Streamlit |
| Charts | Plotly |
| Hosting | Streamlit Community Cloud |

## Run Locally

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deploy to Streamlit Cloud
1. Push this repo to GitHub (must be public)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file to `app.py`
5. Deploy — live link generated automatically

## Dataset
Maven Analytics — Coffee Shop Sales (Jan–Jun 2023)
- 149,116 transactions
- 3 NYC locations: Lower Manhattan, Hell's Kitchen, Astoria
- ~$698K total revenue across 9 product categories