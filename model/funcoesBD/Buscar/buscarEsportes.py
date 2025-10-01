from ..Cadastrar.criarConexao import criarConexao, database

def buscarEsportes():
    conexao = criarConexao()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM esportes")
            return cursor.fetchall()
    finally:
        conexao.close()