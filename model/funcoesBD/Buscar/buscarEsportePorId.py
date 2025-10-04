from ..Cadastrar.criarConexao import criarConexao, database

def buscarEsportePorId(pk_esporte,):
    conn = criarConexao()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT pk_esporte, qtd_jogadores
        FROM esportes
        WHERE pk_esporte = %s
    """
    cursor.execute(query, (pk_esporte,))
    esportes = cursor.fetchone()
    cursor.close()
    conn.close()
    return esportes