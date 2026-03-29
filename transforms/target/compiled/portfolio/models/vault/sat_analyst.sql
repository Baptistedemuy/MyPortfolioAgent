SELECT
    md5(cd_ticker) AS hk_instrument,
    cd_ticker,
    dt_date,
    ingested_at    AS load_dts,
    firm,
    from_grade,
    to_grade,
    action
FROM "portfolio"."main"."raw_analyst_ratings"