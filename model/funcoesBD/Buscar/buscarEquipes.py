from ..Cadastrar.criarConexao import criarConexao, database

def buscarEquipes():
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT pk_equipe, fk_esporte, fk_nome_turma, fk_descricao FROM equipes")
            return cursor.fetchall()
    finally:
        conexao.close()