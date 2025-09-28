from .criarConexao import criarConexao, database

def deletarEquipe(pk_equipe):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM membros_equipe WHERE fk_equipe=%s", (pk_equipe,))
            cursor.execute("DELETE FROM equipes WHERE pk_equipe=%s", (pk_equipe,))
        conexao.commit()
    finally:
        conexao.close()
