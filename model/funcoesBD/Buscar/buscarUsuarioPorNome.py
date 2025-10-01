from ..Cadastrar.criarConexao import criarConexao, database

def buscarUsuarioPorNome(usuario):
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)

    query = "SELECT * FROM login WHERE pk_usuario = %s"
    cursor.execute(query, (usuario,))
    usuario_buscado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario_buscado