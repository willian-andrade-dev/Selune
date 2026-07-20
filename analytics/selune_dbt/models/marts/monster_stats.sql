SELECT
    m.nome AS monstro_nome,
    COUNT(*) AS total_combates,
    SUM(CASE WHEN scl.vitoria THEN 1 ELSE 0 END) AS vitorias,
    ROUND(SUM(CASE WHEN scl.vitoria THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS taxa_vitoria_pct,
    ROUND(AVG(scl.xp_ganho), 2) AS xp_medio,
    ROUND(AVG(scl.gold_ganho), 2) AS gold_medio
FROM {{ ref('stg_combat_logs') }} scl
JOIN {{ source('selune', 'monsters') }} m ON scl.monster_id = m.id
GROUP BY m.nome