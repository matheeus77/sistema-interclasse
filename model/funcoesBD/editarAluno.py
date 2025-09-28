from .criarConexao import criarConexao, database

def editarAluno(matricula, nome, turma, genero):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            query = "UPDATE alunos SET nome_aluno=%s, fk_nome_turma=%s, fk_classificacao=%s WHERE pk_matricula=%s"
            cursor.execute(query, (nome, turma, genero, matricula))
        conexao.commit()
    finally:
        conexao.close()
