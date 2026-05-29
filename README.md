# ☕ PulseBoard — Coffee Shop Sales Dashboard

An interactive sales analytics dashboard built with Streamlit and Plotly, analyzing 149K transactions across 3 New York City coffee shop locations.

## Features
- **KPI Cards** — Total revenue, transactions, avg order value, top location
- **Revenue Over Time** — Monthly trends by location
- **Category Breakdown** — Revenue split across 9 product categories
- **Hourly Traffic** — Peak hours by store location
- **Top 10 Products** — Best performing items by revenue
- **Location Share** — Revenue distribution donut chart
- **Monthly Volume** — Stacked transaction volume by category
- **Sidebar Filters** — Filter by location, category, and date range

## Tech Stack
- Python · Pandas · Streamlit · Plotly

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud
1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy

## Dataset
Maven Analytics — Coffee Shop Sales (Jan–Jun 2023)
- 149,116 transactions
- 3 locations: Lower Manhattan, Hell's Kitchen, Astoria
- ~$698K total revenue