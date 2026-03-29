import yaml
import yfinance as yf
import duckdb
import pandas as pd
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "instrument.yml"
DB_PATH = ROOT / "database" / "portfolio.duckdb"


def load_tickers(config_path) -> list[str]:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config["instruments"]


def get_watermark(conn, ticker: str):
    result = conn.execute(
        "SELECT MAX(dt_date) FROM raw_analyst_ratings WHERE cd_ticker = ?", [ticker]
    ).fetchone()
    return result[0]


def fetch_ratings(ticker: str) -> pd.DataFrame:
    data = yf.Ticker(ticker).upgrades_downgrades
    if data is None or data.empty:
        return pd.DataFrame()

    data = data.reset_index()
    data = data.rename(columns={
        "GradeDate": "dt_date",
        "Firm":      "firm",
        "FromGrade": "from_grade",
        "ToGrade":   "to_grade",
        "Action":    "action",
    })
    data["dt_date"] = pd.to_datetime(data["dt_date"]).dt.date
    data["cd_ticker"] = ticker
    return data[["cd_ticker", "dt_date", "firm", "from_grade", "to_grade", "action"]]


def ingest(tickers: list[str]):
    conn = duckdb.connect(DB_PATH)
    total_rows = 0

    for ticker in tickers:
        watermark = get_watermark(conn, ticker)
        print(f"  {ticker}...", end=" ")

        df = fetch_ratings(ticker)
        if df.empty:
            print("no data, skipped.")
            continue

        if watermark:
            df = df[df["dt_date"] > watermark]

        if df.empty:
            print("already up to date.")
            continue

        conn.execute("""
            INSERT OR REPLACE INTO raw_analyst_ratings
                (cd_ticker, dt_date, firm, from_grade, to_grade, action)
            SELECT cd_ticker, dt_date, firm, from_grade, to_grade, action
            FROM df
        """)
        print(f"{len(df)} rows inserted.")
        total_rows += len(df)

    conn.close()
    print(f"\nDone. {total_rows} rows inserted across {len(tickers)} tickers.")


if __name__ == "__main__":
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Starting analyst ingestion...")
    tickers = load_tickers(CONFIG_PATH)
    print(f"  {len(tickers)} tickers found in config.\n")
    ingest(tickers)
