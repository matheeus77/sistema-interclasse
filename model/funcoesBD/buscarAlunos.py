from .criarConexao import criarConexao, database

def buscarAlunos():
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT pk_matricula, nome_aluno, fk_nome_turma, fk_classificacao FROM alunos")
            return cursor.fetchall()
    finally:
        conexao.close()
