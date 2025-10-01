from ..Cadastrar.criarConexao import criarConexao, database

def editarEquipe(pk_equipe, esporte, turma, descricao, nome_equipe, alunos):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            # Atualizar dados principais
            cursor.execute("""
                UPDATE equipes
                SET fk_esporte=%s, fk_nome_turma=%s, fk_descricao=%s, nome_equipe=%s
                WHERE pk_equipe=%s
            """, (esporte, turma, descricao, nome_equipe, pk_equipe))

            # Apagar jogadores antigos
            cursor.execute("DELETE FROM membros_equipe WHERE fk_equipe=%s", (pk_equipe,))

            # Inserir os novos
            for matricula in alunos:
                cursor.execute("""
                    INSERT INTO membros_equipe (fk_equipe, fk_matricula)
                    VALUES (%s, %s)
                """, (pk_equipe, matricula))

        conexao.commit()
    finally:
        conexao.close()
