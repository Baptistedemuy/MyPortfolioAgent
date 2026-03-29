# MyPortfolioAgent

Pipeline de données + LLM pour analyser un portefeuille boursier : prix historiques, ratings analystes, sentiment et dashboard Streamlit.

## Stack

| Couche | Outil |
|---|---|
| Ingestion | Python + yfinance |
| Stockage | DuckDB |
| Transform | dbt (Data Vault → Star Schema) |
| LLM | À venir |
| Dashboard | Streamlit |

## Structure

```
MyPortfolioAgent/
├── config/
│   └── instrument.yml        # liste des tickers
├── ingestion/
│   ├── ingest_prices.py      # prix OHLCV via yfinance
│   └── ingest_analyst.py     # ratings analystes via yfinance
├── database/
│   ├── init_db.py            # initialisation des tables raw
│   ├── queryDB.py            # requêtes de vérification
│   └── portfolio.duckdb      # base de données locale
├── transforms/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── vault/            # Data Vault (hub + satellites)
│       └── mart/             # Star Schema (dims + facts)
├── dashboard/
│   └── app.py                # Streamlit
└── requirements.txt
```

## Installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
source .venv/bin/activate

# 1. Initialiser la base de données
python database/init_db.py

# 2. Ingérer les données
python ingestion/ingest_prices.py
python ingestion/ingest_analyst.py

# 3. Lancer les transformations dbt
cd transforms
dbt run --profiles-dir .
cd ..

# 4. Lancer le dashboard
streamlit run dashboard/app.py
```
