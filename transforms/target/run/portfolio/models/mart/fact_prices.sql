
  
    
    

    create  table
      "portfolio"."mart"."fact_prices__dbt_tmp"
  
    as (
      SELECT
    sp.hk_instrument                                  AS sk_instrument,
    CAST(STRFTIME(sp.dt_date, '%Y%m%d') AS INTEGER)  AS sk_date,
    sp.cd_open,
    sp.cd_high,
    sp.cd_low,
    sp.cd_close,
    sp.cd_adj_close,
    sp.nb_volume
FROM "portfolio"."vault"."sat_prices" sp
    );
  
  