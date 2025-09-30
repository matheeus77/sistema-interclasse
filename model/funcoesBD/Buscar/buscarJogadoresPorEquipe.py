from ..Cadastrar.criarConexao import criarConexao, database

def buscarJogadoresPorEquipe(id_equipe):
    conexao = criarConexao()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            query = """
                SELECT a.pk_matricula AS matricula,
                       a.nome_aluno AS nome
                FROM membros_equipe me
                JOIN alunos a ON me.fk_matricula = a.pk_matricula
                WHERE me.fk_equipe = %s
            """
            cursor.execute(query, (id_equipe,))
            return cursor.fetchall()
    finally:
        conexao.close()