SELECT
    hk_instrument AS sk_instrument,
    cd_ticker,
    CASE
        WHEN cd_ticker LIKE '%.AS' OR cd_ticker LIKE '%.BR' THEN 'EU'
        ELSE 'US'
    END AS market
FROM {{ ref('hub_instrument') }}
