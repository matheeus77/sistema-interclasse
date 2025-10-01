from ..Cadastrar.criarConexao import criarConexao, database

def telaUsuarios():
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM login")
            return cursor.fetchall()
    finally:
        conexao.close()