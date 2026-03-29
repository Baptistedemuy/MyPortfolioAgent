import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "portfolio.duckdb"
conn = duckdb.connect(str(DB_PATH))
df = conn.execute("SELECT * FROM raw_prices LIMIT 10").fetchdf() 
print(df)
