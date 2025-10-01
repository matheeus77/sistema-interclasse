from ..Cadastrar.criarConexao import criarConexao, database

# Buscar alunos de uma turma
def alunosPorTurmaListaEquipes(nome_turma, classificacao):
    conexao = criarConexao()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            if classificacao == "Mista":
                query = """
                    SELECT pk_matricula AS matricula,
                           nome_aluno AS nome
                    FROM alunos
                    WHERE fk_nome_turma = %s
                """
                cursor.execute(query, (nome_turma,))
            else:
                query = """
                    SELECT pk_matricula AS matricula,
                           nome_aluno AS nome
                    FROM alunos
                    WHERE fk_nome_turma = %s
                      AND fk_classificacao = %s
                """
                cursor.execute(query, (nome_turma, classificacao))

            return cursor.fetchall()
    finally:
        conexao.close()
