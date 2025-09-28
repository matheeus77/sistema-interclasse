from .criarConexao import criarConexao, database

def buscarEstatisticasPorId(idPartida):
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(f'''SELECT * FROM {database}.estatisticas_partida WHERE fk_partida = %s ORDER BY fk_partida, 
                        CASE
                            WHEN fk_nome_estatistica IN ('Gols', 'Pontos') THEN 1
                            WHEN fk_nome_estatistica IN ('Finalizações', 'Arremessos de Três') THEN 2
                            WHEN fk_nome_estatistica IN ('Passes', 'Rebotes') THEN 3
                            ELSE 4
                        END;''', (idPartida,))
    partidasComEstatisticas = cursor.fetchall()

    return partidasComEstatisticas