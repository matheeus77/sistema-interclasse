from .criarConexao import criarConexao, database

def cadastrarEsportes(esporte):
    conexao = criarConexao()
    cursor = conexao.cursor()

    cursor.execute(f'INSERT INTO {database}.esportes (pk_esporte) values (%s)', (esporte,))
    conexao.commit()

    cursor.close()
    conexao.close()

    return print('Cadastrado com sucesso')


