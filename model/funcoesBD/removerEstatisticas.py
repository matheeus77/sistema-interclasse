from .criarConexao import criarConexao, database

def removerEstatisticas(estatistica):
    conexao = criarConexao()
    cursor = conexao.cursor()

    cursor.execute(f'DELETE FROM {database}.tipo_estatistica WHERE pk_nome_estatistica = %s', (estatistica,))
    conexao.commit()

    cursor.close()
    conexao.close()