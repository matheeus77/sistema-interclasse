from ..Cadastrar.criarConexao import criarConexao, database

def buscarEquipes():
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            query = """
                SELECT e.pk_equipe,
                       s.pk_esporte AS esporte,
                       t.pk_nome_turma AS turma,
                       c.pk_descricao AS classificacao,
                       e.nome_equipe
                FROM equipes e
                JOIN esportes s ON e.fk_esporte = s.pk_esporte
                JOIN turmas t ON e.fk_nome_turma = t.pk_nome_turma
                JOIN classificacao c ON e.fk_descricao = c.pk_descricao
            """
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        conexao.close()
