from .criarConexao import criarConexao, database

def buscarClassificacoes():
    conexao = criarConexao()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT pk_descricao FROM classificacao")
            return cursor.fetchall()
    finally:
        conexao.close()