import duckdb
conn = duckdb.connect("database/portfolio.duckdb")
df = conn.execute("SELECT * FROM raw_prices LIMIT 10").fetchdf() 
print(df)
