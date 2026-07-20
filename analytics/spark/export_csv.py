
from Database.connection import conectar

def exportar_combat_logs_csv(caminho='analytics/spark/dados/combat_logs.csv'):
    conexao = conectar()
    cursor = conexao.cursor()

    with open(caminho, 'w') as arquivo:
        cursor.copy_expert("""
            COPY (
                SELECT cl.id, cl.player_id, cl.monster_id, m.nome AS monstro_nome,
                       cl.xp_ganho, cl.gold_ganho,
                       CASE WHEN cl.vitoria THEN 'true' ELSE 'false' END as vitoria, 
                       cl.duracao_ms, cl.data_hora
                FROM combat_logs cl
                JOIN monsters m ON cl.monster_id = m.id
            ) TO STDOUT WITH (FORMAT csv, HEADER true, DELIMITER ';')
        """, arquivo)

    cursor.close()
    conexao.close()
    print(f"Exportado para {caminho}")

if __name__ == "__main__":
    exportar_combat_logs_csv()