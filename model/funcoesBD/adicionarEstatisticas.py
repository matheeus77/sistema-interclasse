from .criarConexao import criarConexao, database

def adicionarEstatisticas(id_partida, nome_estatistica, valor_time_casa, valor_time_visitante):
    conexao = criarConexao()
    cursor = conexao.cursor()
    cursor.execute(f'UPDATE {database}.estatisticas_partida SET valor_time_casa = %s, valor_time_visitante = %s WHERE fk_partida = %s AND fk_nome_estatistica = %s', (valor_time_casa, valor_time_visitante, id_partida, nome_estatistica))

    conexao.commit()

    cursor.close()
    conexao.close()
    print('Dados adicionados')