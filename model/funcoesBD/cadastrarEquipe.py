from .criarConexao import criarConexao, database

def cadastrarEquipe(esporte, turma, descricao, alunos):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                INSERT INTO equipes (fk_esporte, fk_nome_turma, fk_descricao)
                VALUES (%s, %s, %s)
            """, (esporte, turma, descricao))
            id_equipe = cursor.lastrowid

            for matricula in alunos:
                cursor.execute("""
                    INSERT INTO membros_equipe (fk_equipe, fk_matricula)
                    VALUES (%s, %s)
                """, (id_equipe, matricula))

        conexao.commit()
    finally:
        conexao.close()