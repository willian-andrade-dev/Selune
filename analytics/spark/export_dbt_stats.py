from Database.connection import conectar

def exportar_monster_stats_csv(caminho='analytics/spark/dados/monster_stats.csv'):
    conexao = conectar()
    cursor = conexao.cursor()

# ESTOU UTILIZANDO REPLACE DEVIDO O POWER BI ESTAR COM A LOCALIDADE 
    with open(caminho, 'w') as arquivo:
        cursor.copy_expert("""
            COPY (
                SELECT 
                    monstro_nome, 
                    total_combates, 
                    vitorias, 
                    REPLACE(taxa_vitoria_pct::text, '.', ',') AS taxa_vitoria_pct,
                    REPLACE(xp_medio::text, '.', ',') AS xp_medio,
                    REPLACE(gold_medio::text, '.', ',') AS gold_medio
                FROM monster_stats
            ) TO STDOUT WITH (FORMAT csv, HEADER true, DELIMITER ';')
        """, arquivo)

    cursor.close()
    conexao.close()
    print(f"Exportado para {caminho}")

if __name__ == "__main__":
    exportar_monster_stats_csv()