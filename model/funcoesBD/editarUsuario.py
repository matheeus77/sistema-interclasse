from .criarConexao import criarConexao, database

def editarUsuario(pk_usuario_antigo, pk_usuario_novo, senha, nivel, fk_nome_turma=None):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            if senha and senha.strip() != "":
                query = """
                    UPDATE login
                    SET pk_usuario=%s, senha=%s, nivel=%s, fk_nome_turma=%s
                    WHERE pk_usuario=%s
                """
                cursor.execute(query, (pk_usuario_novo, senha, nivel, fk_nome_turma, pk_usuario_antigo))
            else:
                query = """
                    UPDATE login
                    SET pk_usuario=%s, nivel=%s, fk_nome_turma=%s
                    WHERE pk_usuario=%s
                """
                cursor.execute(query, (pk_usuario_novo, nivel, fk_nome_turma, pk_usuario_antigo))
        conexao.commit()
    finally:
        conexao.close()