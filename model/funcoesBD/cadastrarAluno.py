from .criarConexao import criarConexao, database

def cadastrarAluno(matricula, nome, turma, genero):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            query = """
                INSERT INTO alunos (pk_matricula, nome_aluno, fk_nome_turma, fk_classificacao)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (matricula, nome, turma, genero))
        conexao.commit()
    finally:
        conexao.close()
