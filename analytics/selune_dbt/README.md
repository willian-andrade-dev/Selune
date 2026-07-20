# Selune dbt

Camada de transformação de dados do projeto Selune.

## Models

- `staging/stg_combat_logs` — view limpa sobre a tabela bruta `combat_logs`
- `marts/monster_stats` — estatísticas agregadas por monstro (total de combates, taxa de vitória, XP/gold médios)

## Rodando

```bash
export $(cat ../../.env | xargs)  # ou: set -a; source ../../.env; set +a
dbt run
dbt test
```