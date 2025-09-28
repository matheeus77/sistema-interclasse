from .criarConexao import criarConexao, database

def buscarUsuarios(login, senha):
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM login where pk_usuario = %s and senha = %s', (login, senha))

    usuariosBuscados = cursor.fetchone()
    print(usuariosBuscados)
    cursor.close()
    conexao.close()
    return usuariosBuscados
