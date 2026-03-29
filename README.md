# MyPortfolioAgent

Pipeline de données + LLM pour analyser un portefeuille boursier : prix historiques, news, sentiment, résumés quotidiens et dashboard Streamlit.

## Structure

```
MyPortfolioAgent/
├── config/                   # yml
├── ingestion/                # python
├── database/
│   └── portfolio.duckdb      # stockage local
├── transforms/               # modèles dbt
├── llm/
│   └── summarizer.py         # résumé quotidien via Ollama (Mistral)
├── dashboard/
│   └── app.py                # Streamlit
└── README.md
```

## Stack

| Couche | Outil |
|---|---|
| Ingestion | python |
| Stockage | DuckDB |
| Transform | dbt |
| LLM |  |
| Dashboard |  |

## Plan and technologic choice

We will collect data from yfinance, because it's free, and no API key required.

We will stock the data into a DuckDB -> It's an SQL database, very easy to set up


The ingestion technology will be in python to collect the data from yfinance and ingest into the DuckDB tables

And to make the transformation we will use dbt to orchestrate the steps easily

## Installation

```bash
# Créer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  

# Installer les dépendances
pip install -r requirements.txt


#Activer
source .venv/bin/activate
#desactiver
deactivate
```


## Initialisation de la base de données

```bash
python database/init_db.py
```

To install to query the db : extension DuckDB dans vsCode
## Initialiser venv

