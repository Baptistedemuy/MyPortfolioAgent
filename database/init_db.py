import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "portfolio.duckdb"

conn = duckdb.connect(DB_PATH)

conn.execute("""
    CREATE TABLE IF NOT EXISTS raw_prices (
        cd_ticker      TEXT,
        dt_date        DATE,
        cd_open        DOUBLE,
        cd_high        DOUBLE,
        cd_low         DOUBLE,
        cd_close       DOUBLE,
        cd_adj_close   DOUBLE,
        nb_volume      BIGINT,
        ingested_at TIMESTAMP DEFAULT now(),
        PRIMARY KEY (cd_ticker, dt_date)
    )
""")


conn.execute("""
    CREATE TABLE IF NOT EXISTS raw_analyst_ratings (
        cd_ticker   TEXT,
        dt_date     DATE,
        firm        TEXT,
        from_grade  TEXT,
        to_grade    TEXT,
        action      TEXT,
        ingested_at TIMESTAMP DEFAULT now(),
        PRIMARY KEY (cd_ticker, dt_date, firm)
    )
""")

conn.close()
print(f"Base de données initialisée : {DB_PATH}")
