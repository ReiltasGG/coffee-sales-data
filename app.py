import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PulseBoard | Coffee Sales",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Root palette */
:root {
    --bg:        #0f0e0c;
    --surface:   #1a1814;
    --border:    #2e2b26;
    --gold:      #c9a84c;
    --gold-dim:  #8a6f2e;
    --cream:     #f0e6d0;
    --muted:     #7a7060;
    --red:       #c94c4c;
    --green:     #4caf82;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--cream) !important; }

/* Header strip */
.header-strip {
    display: flex;
    align-items: baseline;
    gap: 12px;
    padding: 0 0 28px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}
.header-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: var(--gold);
    letter-spacing: -1px;
}
.header-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* KPI cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--gold);
    border-radius: 3px 0 0 3px;
}
.kpi-label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--cream);
    line-height: 1;
}
.kpi-delta {
    font-size: 0.78rem;
    color: var(--green);
    margin-top: 6px;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold);
    margin-bottom: 12px;
}

/* Divider */
.divider { border-top: 1px solid var(--border); margin: 28px 0; }

/* Sidebar label override */
.sidebar-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold-dim);
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE_DIR, "Coffee_Shop_Sales.xlsx"))
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["revenue"] = df["transaction_qty"] * df["unit_price"]
    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["month_name"] = df["transaction_date"].dt.strftime("%b %Y")
    df["hour"] = df["transaction_time"].apply(lambda t: t.hour if hasattr(t, 'hour') else pd.to_datetime(str(t)).hour)
    return df

df = load_data()

# ── Plotly dark theme ─────────────────────────────────────────────────────────
COLORS   = ["#c9a84c", "#4caf82", "#6b9fd4", "#c94c4c", "#a06bc9", "#d4946b", "#6bc9c9", "#c9c96b"]
BG_COLOR = "#0f0e0c"
SURFACE  = "#1a1814"
GRID     = "#2e2b26"
TEXT     = "#f0e6d0"
MUTED    = "#7a7060"

def dark_layout(fig, title=""):
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=SURFACE,
        font=dict(family="DM Sans", color=TEXT, size=12),
        title=dict(text=title, font=dict(family="Syne", size=15, color=TEXT), x=0, xanchor="left"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID, font=dict(size=11)),
        margin=dict(l=8, r=8, t=40 if title else 8, b=8),
        xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED)),
    )
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">☕ PulseBoard</p>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<p class="sidebar-title">Location</p>', unsafe_allow_html=True)
    all_locations = sorted(df["store_location"].unique())
    selected_locations = st.multiselect(
        label="location",
        options=all_locations,
        default=all_locations,
        label_visibility="collapsed",
    )

    st.markdown('<p class="sidebar-title">Category</p>', unsafe_allow_html=True)
    all_cats = sorted(df["product_category"].unique())
    selected_cats = st.multiselect(
        label="category",
        options=all_cats,
        default=all_cats,
        label_visibility="collapsed",
    )

    st.markdown('<p class="sidebar-title">Date Range</p>', unsafe_allow_html=True)
    min_date = df["transaction_date"].min().date()
    max_date = df["transaction_date"].max().date()
    date_range = st.date_input(
        label="dates",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f'<p style="font-size:0.7rem;color:#7a7060;">Dataset · 149K transactions<br>Jan–Jun 2023 · 3 locations</p>', unsafe_allow_html=True)

# ── Filter data ───────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start, end = df["transaction_date"].min(), df["transaction_date"].max()

fdf = df[
    df["store_location"].isin(selected_locations) &
    df["product_category"].isin(selected_cats) &
    df["transaction_date"].between(start, end)
]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-strip">
    <span class="header-logo">PulseBoard</span>
    <span class="header-sub">Coffee Shop Analytics · 2023</span>
</div>
""", unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
total_rev   = fdf["revenue"].sum()
total_orders = fdf["transaction_id"].nunique()
avg_order   = total_rev / total_orders if total_orders else 0
top_location = fdf.groupby("store_location")["revenue"].sum().idxmax() if not fdf.empty else "—"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value">${total_rev:,.0f}</div>
    <div class="kpi-delta">Jan – Jun 2023</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Total Transactions</div>
    <div class="kpi-value">{total_orders:,}</div>
    <div class="kpi-delta">Unique orders</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Avg Order Value</div>
    <div class="kpi-value">${avg_order:.2f}</div>
    <div class="kpi-delta">Per transaction</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Top Location</div>
    <div class="kpi-value" style="font-size:1.2rem;padding-top:6px">{top_location}</div>
    <div class="kpi-delta">By revenue</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Row 1: Revenue over time + by category ────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<p class="section-label">Revenue Over Time by Location</p>', unsafe_allow_html=True)
    monthly = (
        fdf.groupby(["month", "month_name", "store_location"])["revenue"]
        .sum().reset_index()
        .sort_values("month")
    )
    fig1 = px.line(
        monthly, x="month_name", y="revenue",
        color="store_location",
        color_discrete_sequence=COLORS,
        markers=True,
    )
    fig1.update_traces(line=dict(width=2.5), marker=dict(size=6))
    fig1.update_layout(
        xaxis_title="", yaxis_title="Revenue ($)",
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
    )
    dark_layout(fig1)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown('<p class="section-label">Revenue by Category</p>', unsafe_allow_html=True)
    cat_rev = (
        fdf.groupby("product_category")["revenue"]
        .sum().reset_index()
        .sort_values("revenue", ascending=True)
    )
    fig2 = px.bar(
        cat_rev, x="revenue", y="product_category",
        orientation="h",
        color="revenue",
        color_continuous_scale=[[0, "#2e2b26"], [1, "#c9a84c"]],
    )
    fig2.update_layout(
        xaxis_title="Revenue ($)", yaxis_title="",
        xaxis_tickprefix="$", xaxis_tickformat=",.0f",
        coloraxis_showscale=False,
    )
    dark_layout(fig2)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Row 2: Hourly traffic + Top products ─────────────────────────────────────
col3, col4 = st.columns([2, 3])

with col3:
    st.markdown('<p class="section-label">Busiest Hours by Location</p>', unsafe_allow_html=True)
    hourly = (
        fdf.groupby(["hour", "store_location"])["transaction_id"]
        .count().reset_index()
        .rename(columns={"transaction_id": "transactions"})
    )
    fig3 = px.line(
        hourly, x="hour", y="transactions",
        color="store_location",
        color_discrete_sequence=COLORS,
        markers=True,
    )
    fig3.update_traces(line=dict(width=2.5), marker=dict(size=5))
    fig3.update_layout(
        xaxis_title="Hour of Day", yaxis_title="Transactions",
        xaxis=dict(tickmode="linear", dtick=2),
    )
    dark_layout(fig3)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<p class="section-label">Top 10 Products by Revenue</p>', unsafe_allow_html=True)
    top_products = (
        fdf.groupby("product_detail")["revenue"]
        .sum().reset_index()
        .sort_values("revenue", ascending=False)
        .head(10)
        .sort_values("revenue", ascending=True)
    )
    fig4 = px.bar(
        top_products, x="revenue", y="product_detail",
        orientation="h",
        color_discrete_sequence=["#c9a84c"],
    )
    fig4.update_layout(
        xaxis_title="Revenue ($)", yaxis_title="",
        xaxis_tickprefix="$", xaxis_tickformat=",.0f",
    )
    dark_layout(fig4)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Row 3: Location breakdown donut + monthly orders ─────────────────────────
col5, col6 = st.columns([1, 2])

with col5:
    st.markdown('<p class="section-label">Revenue Share by Location</p>', unsafe_allow_html=True)
    loc_rev = fdf.groupby("store_location")["revenue"].sum().reset_index()
    fig5 = px.pie(
        loc_rev, values="revenue", names="store_location",
        hole=0.6,
        color_discrete_sequence=COLORS,
    )
    fig5.update_traces(textfont=dict(color=TEXT), pull=[0.02, 0.02, 0.02])
    fig5.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        paper_bgcolor=BG_COLOR,
        font=dict(family="DM Sans", color=TEXT),
        margin=dict(l=8, r=8, t=8, b=8),
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown('<p class="section-label">Monthly Transaction Volume by Category</p>', unsafe_allow_html=True)
    monthly_cat = (
        fdf.groupby(["month", "month_name", "product_category"])["transaction_id"]
        .count().reset_index()
        .rename(columns={"transaction_id": "transactions"})
        .sort_values("month")
    )
    fig6 = px.bar(
        monthly_cat, x="month_name", y="transactions",
        color="product_category",
        color_discrete_sequence=COLORS,
        barmode="stack",
    )
    fig6.update_layout(xaxis_title="", yaxis_title="Transactions")
    dark_layout(fig6)
    st.plotly_chart(fig6, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:24px 0 8px;color:#3a3530;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;">
PulseBoard · Built with Streamlit · Coffee Shop Sales 2023
</div>
""", unsafe_allow_html=True)