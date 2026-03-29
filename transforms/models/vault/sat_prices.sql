SELECT
    md5(cd_ticker) AS hk_instrument,
    cd_ticker,
    dt_date,
    ingested_at    AS load_dts,
    cd_open,
    cd_high,
    cd_low,
    cd_close,
    cd_adj_close,
    nb_volume
FROM {{ source('raw', 'raw_prices') }}
