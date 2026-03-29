import yaml
import yfinance as yf
import duckdb
import pandas as pd
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "instrument.yml"
DB_PATH = ROOT / "database" / "portfolio.duckdb"


def load_tickers(config_path: str) -> list[str]:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config["instruments"]


def get_watermark(conn: duckdb.DuckDBPyConnection, ticker: str):
    result = conn.execute(
        "SELECT MAX(dt_date) FROM raw_prices WHERE cd_ticker = ?", [ticker]
    ).fetchone()
    return result[0]


def fetch_prices(ticker: str, start_date=None) -> pd.DataFrame:
    if start_date:
        data = yf.download(ticker, start=start_date, auto_adjust=False, progress=False)
    else:
        data = yf.download(ticker, period="max", auto_adjust=False, progress=False)

    if data.empty:
        return pd.DataFrame()

    data = data.reset_index()
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    df = pd.DataFrame({
        "cd_ticker":    ticker,
        "dt_date":      pd.to_datetime(data["Date"]).dt.date,
        "cd_open":      data["Open"].astype(float),
        "cd_high":      data["High"].astype(float),
        "cd_low":       data["Low"].astype(float),
        "cd_close":     data["Close"].astype(float),
        "cd_adj_close": data["Adj Close"].astype(float),
        "nb_volume":    data["Volume"].astype("Int64"),
    })
    return df


def ingest(tickers: list[str]):
    conn = duckdb.connect(DB_PATH)
    total_rows = 0

    for ticker in tickers:
        watermark = get_watermark(conn, ticker)
        if watermark:
            start_date = watermark + pd.Timedelta(days=1)
            print(f"  {ticker}: delta load from {start_date}...", end=" ")
        else:
            start_date = None
            print(f"  {ticker}: full load...", end=" ")

        df = fetch_prices(ticker, start_date)
        if watermark:
            df = df[df["dt_date"] > watermark]
        if df.empty:
            print("already up to date.")
            continue

        conn.execute("""
            INSERT OR REPLACE INTO raw_prices
                (cd_ticker, dt_date, cd_open, cd_high, cd_low, cd_close, cd_adj_close, nb_volume)
            SELECT cd_ticker, dt_date, cd_open, cd_high, cd_low, cd_close, cd_adj_close, nb_volume
            FROM df
        """)
        print(f"{len(df)} rows inserted.")
        total_rows += len(df)

    conn.close()
    print(f"\nDone. {total_rows} rows inserted across {len(tickers)} tickers.")


if __name__ == "__main__":
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Starting ingestion...")
    tickers = load_tickers(CONFIG_PATH)
    print(f"  {len(tickers)} tickers found in config.\n")
    ingest(tickers)
