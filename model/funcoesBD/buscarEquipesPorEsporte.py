from .criarConexao import criarConexao, database

def buscarEquipesPorEsporte(pk_esporte):
    conn = criarConexao()
    cursor = conn.cursor()

    query = """
        SELECT pk_equipe, e.nome, fk_nome_turma AS turma, c.descricao
        FROM equipe e
        INNER JOIN turma t ON e.fk_turma = t.pk_turma
        LEFT JOIN classificacao c ON e.fk_classificacao = c.pk_classificacao
        WHERE e.fk_esporte = %s
    """
    cursor.execute(query, (pk_esporte,))
    equipes = cursor.fetchall()

    cursor.close()
    conn.close()
    return equipes
