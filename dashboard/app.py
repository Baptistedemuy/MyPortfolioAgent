import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "portfolio.duckdb"

st.title("Portfolio Dashboard")


@st.cache_data
def load_tickers():
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    tickers = conn.execute("SELECT DISTINCT cd_ticker FROM raw_prices ORDER BY cd_ticker").df()
    conn.close()
    return tickers["cd_ticker"].tolist()


@st.cache_data
def load_prices(ticker: str) -> pd.DataFrame:
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    df = conn.execute(
        "SELECT dt_date, cd_adj_close, nb_volume FROM raw_prices WHERE cd_ticker = ? ORDER BY dt_date",
        [ticker]
    ).df()
    conn.close()
    return df


@st.cache_data
def load_analyst(ticker: str) -> pd.DataFrame:
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = conn.execute(
            "SELECT dt_date, firm, from_grade, to_grade, action FROM raw_analyst_ratings WHERE cd_ticker = ? ORDER BY dt_date",
            [ticker]
        ).df()
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df


tickers = load_tickers()
ticker = st.selectbox("Ticker", tickers)

prices = load_prices(ticker)
analyst = load_analyst(ticker)

# — Analyst firm filter
selected_firms = []
if not analyst.empty:
    all_firms = sorted(analyst["firm"].unique().tolist())
    selected_firms = st.multiselect("Analyst firms", all_firms, default=all_firms)
    analyst_filtered = analyst[analyst["firm"].isin(selected_firms)]
else:
    analyst_filtered = analyst

# — Closing price + analyst markers
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=prices["dt_date"],
    y=prices["cd_adj_close"],
    mode="lines",
    name="Adj Close",
    line=dict(color="#1f77b4"),
))

if not analyst_filtered.empty:
    color_map = {"up": "green", "down": "red", "init": "orange", "reit": "gray"}
    for _, row in analyst_filtered.iterrows():
        price_row = prices[prices["dt_date"] == row["dt_date"]]
        if price_row.empty:
            continue
        price_val = price_row["cd_adj_close"].iloc[0]
        color = color_map.get(str(row["action"]).lower(), "gray")
        fig.add_trace(go.Scatter(
            x=[row["dt_date"]],
            y=[price_val],
            mode="markers",
            marker=dict(size=6, color=color, symbol="triangle-up"),
            name=row["firm"],
            hovertemplate=f"<b>{row['firm']}</b><br>{row['from_grade']} → {row['to_grade']}<br>Action: {row['action']}<extra></extra>",
            showlegend=False,
        ))

fig.update_layout(
    title=f"{ticker} — Adjusted Close Price",
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

# — Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Last close", f"{prices['cd_adj_close'].iloc[-1]:.2f}")
col2.metric("Last date", str(prices["dt_date"].iloc[-1]))
col3.metric("Analyst events", len(analyst_filtered))

# — Volume
st.subheader("Volume")
st.bar_chart(prices.set_index("dt_date")["nb_volume"])

# — Analyst ratings table
if not analyst_filtered.empty:
    st.subheader("Analyst Ratings")
    st.dataframe(analyst_filtered.sort_values("dt_date", ascending=False), use_container_width=True)
