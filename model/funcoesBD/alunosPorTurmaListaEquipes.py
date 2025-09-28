from .criarConexao import criarConexao, database

# Buscar alunos de uma turma
def alunosPorTurmaListaEquipes(nome_turma):
    conexao = criarConexao()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            query = """
                SELECT pk_matricula AS matricula,
                       nome_aluno AS nome
                FROM alunos
                WHERE fk_nome_turma = %s
            """
            cursor.execute(query, (nome_turma,))
            return cursor.fetchall()
    finally:
        conexao.close()