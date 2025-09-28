from .criarConexao import criarConexao, database

def deletarAluno(matricula):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM alunos WHERE pk_matricula=%s", (matricula,))
        conexao.commit()
    finally:
        conexao.close()
