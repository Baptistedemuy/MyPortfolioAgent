
  
    
    

    create  table
      "portfolio"."mart"."dim_date__dbt_tmp"
  
    as (
      SELECT DISTINCT
    CAST(STRFTIME(dt_date, '%Y%m%d') AS INTEGER) AS sk_date,
    dt_date,
    YEAR(dt_date)      AS year,
    MONTH(dt_date)     AS month,
    DAY(dt_date)       AS day,
    DAYOFWEEK(dt_date) AS day_of_week
FROM "portfolio"."vault"."sat_prices"
    );
  
  