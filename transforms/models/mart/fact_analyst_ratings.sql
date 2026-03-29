SELECT
    sa.hk_instrument                                  AS sk_instrument,
    CAST(STRFTIME(sa.dt_date, '%Y%m%d') AS INTEGER)  AS sk_date,
    sa.firm,
    sa.from_grade,
    sa.to_grade,
    sa.action
FROM {{ ref('sat_analyst') }} sa
