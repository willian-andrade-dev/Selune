SELECT
    id,
    player_id,
    monster_id,
    xp_ganho,
    gold_ganho,
    vitoria,
    duracao_ms,
    data_hora
FROM {{ source('selune', 'combat_logs') }}