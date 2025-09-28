from .criarConexao import criarConexao, database

def removerModalidade(esporte):
    conexao = criarConexao()
    cursor = conexao.cursor()

    cursor.execute(f'DELETE FROM {database}.esportes WHERE pk_esporte = %s', (esporte,))
    conexao.commit()

    cursor.close()
    conexao.close()