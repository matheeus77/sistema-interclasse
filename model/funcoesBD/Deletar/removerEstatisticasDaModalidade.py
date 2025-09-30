from ..Cadastrar.criarConexao import criarConexao, database

def removerEstatisticasDaModalidade(esporte,estatistica):
    conexao = criarConexao()
    cursor = conexao.cursor()

    cursor.execute(f'DELETE FROM {database}.estatisticas_esporte WHERE fk_esporte = %s and fk_nome_estatistica = %s', (esporte, estatistica))
    conexao.commit()

    cursor.close()
    conexao.close()