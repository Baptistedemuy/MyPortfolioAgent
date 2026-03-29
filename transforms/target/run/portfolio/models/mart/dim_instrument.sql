
  
    
    

    create  table
      "portfolio"."mart"."dim_instrument__dbt_tmp"
  
    as (
      SELECT
    hk_instrument AS sk_instrument,
    cd_ticker,
    CASE
        WHEN cd_ticker LIKE '%.AS' OR cd_ticker LIKE '%.BR' THEN 'EU'
        ELSE 'US'
    END AS market
FROM "portfolio"."vault"."hub_instrument"
    );
  
  