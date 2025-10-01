from ..Cadastrar.criarConexao import criarConexao, database

def deletarUsuario(pk_usuario):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM login WHERE pk_usuario=%s", (pk_usuario,))
        conexao.commit()
    finally:
        conexao.close()