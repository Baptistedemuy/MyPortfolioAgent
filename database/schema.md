# Data Model

## Table : raw_prices

Stores raw OHLCV daily prices fetched from yfinance.

| Column       | Type      | Description                        |
|--------------|-----------|------------------------------------|
| cd_ticker    | TEXT      | Instrument ticker (e.g. MSFT)      |
| dt_date      | DATE      | Price date                         |
| cd_open      | DOUBLE    | Opening price                      |
| cd_high      | DOUBLE    | Highest price of the day           |
| cd_low       | DOUBLE    | Lowest price of the day            |
| cd_close     | DOUBLE    | Closing price                      |
| cd_adj_close | DOUBLE    | Adjusted closing price             |
| nb_volume    | BIGINT    | Volume traded                      |
| ingested_at  | TIMESTAMP | Timestamp of ingestion (auto-set)  |

**Primary key:** (cd_ticker, dt_date)

## Watermark strategy

Before fetching, we query `MAX(dt_date)` per ticker in `raw_prices`.
- If data exists → fetch only from `last_date + 1 day` (delta load)
- If no data → fetch full history with `period="max"` (initial load)
