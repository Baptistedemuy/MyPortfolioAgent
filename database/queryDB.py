import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "portfolio.duckdb"
conn = duckdb.connect(str(DB_PATH))
df = conn.execute("SELECT * FROM raw_prices ORDER BY dt_date DESC LIMIT 10").fetchdf() 
print(df)
df1 = conn.execute("SELECT distinct cd_ticker FROM raw_prices ").fetchdf() 
print(df1)
df1 = conn.execute("SELECT * FROM raw_prices WHERE cd_ticker ='SAP' ORDER BY dt_date DESC LIMIT 10").fetchdf() 
print(df1)