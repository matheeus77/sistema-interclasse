from .criarConexao import criarConexao, database
from .buscarEstatisticasPorModalidade import buscarEstatisticasPorModalidade

def criarPartidas(esporte, descricao, turma_casa, turma_visitante, dia):
    conexao = criarConexao()
    cursor = conexao.cursor()
    cursor.execute(f"""
        INSERT INTO {database}.partidas (fk_esporte, fk_descricao, fk_turma_casa, pontos_turma_casa, fk_turma_visitante, pontos_turma_visitante)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (esporte, descricao, turma_casa, 0, turma_visitante, 0))

    idNovaPartida = cursor.lastrowid

    conexao.commit()

    cursor.execute(f'INSERT INTO {database}.calendario (dia_evento, fk_partida) values (%s,%s)', (dia, idNovaPartida))

    conexao.commit()

    for nome_estatistica in buscarEstatisticasPorModalidade(esporte):
        cursor.execute(f'insert into {database}.estatisticas_partida (fk_partida, fk_nome_estatistica, valor_time_casa, valor_time_visitante) values (%s,%s,%s,%s)', (idNovaPartida, nome_estatistica['fk_nome_estatistica'], 0, 0))

        conexao.commit()

    cursor.close()
    conexao.close()
    print("✅ Partida criada com sucesso!")