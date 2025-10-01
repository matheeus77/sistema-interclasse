from ..Cadastrar.criarConexao import criarConexao, database

def editarEquipe(pk_equipe, esporte, turma, descricao, alunos):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                UPDATE equipes
                SET fk_esporte=%s, fk_nome_turma=%s, fk_descricao=%s
                WHERE pk_equipe=%s
            """, (esporte, turma, descricao, pk_equipe))

            cursor.execute("DELETE FROM membros_equipe WHERE fk_equipe=%s", (pk_equipe,))

            for matricula in alunos:
                cursor.execute("""
                    INSERT INTO membros_equipe (fk_equipe, fk_matricula)
                    VALUES (%s, %s)
                """, (pk_equipe, matricula))

        conexao.commit()
    finally:
        conexao.close()
