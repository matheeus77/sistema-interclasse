from .criarConexao import criarConexao, database

def buscarPartidaPorId(id):
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(f'SELECT * FROM {database}.partidas WHERE pk_partida = %s', (id,))
    partidaBuscada = cursor.fetchone()
    cursor.close()
    conexao.close()

    return partidaBuscada