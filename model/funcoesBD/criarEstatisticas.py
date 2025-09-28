from .criarConexao import criarConexao, database

def criarEstatisticas(nomeDaEstatistica):
    conexao = criarConexao()
    cursor = conexao.cursor()
    cursor.execute(f'INSERT INTO {database}.tipo_estatistica(pk_nome_estatistica) values (%s)', (nomeDaEstatistica,))

    conexao.commit()

    cursor.close()
    conexao.close()