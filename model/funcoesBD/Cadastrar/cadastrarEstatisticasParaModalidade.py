from .criarConexao import criarConexao, database

def cadastrarEstatisticasParaModalidade(esporte,estatistica):
    conexao = criarConexao()
    cursor = conexao.cursor()

    cursor.execute(f'INSERT INTO {database}.estatisticas_esporte (fk_esporte, fk_nome_estatistica) values (%s,%s)', (esporte, estatistica))
    conexao.commit()

    cursor.close()
    conexao.close()

    return print('Cadastrado com sucesso')