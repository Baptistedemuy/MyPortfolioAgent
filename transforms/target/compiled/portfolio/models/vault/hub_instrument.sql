SELECT
    md5(cd_ticker)   AS hk_instrument,
    cd_ticker,
    MIN(ingested_at) AS load_dts,
    'yfinance'       AS rec_src
FROM "portfolio"."main"."raw_prices"
GROUP BY cd_ticker