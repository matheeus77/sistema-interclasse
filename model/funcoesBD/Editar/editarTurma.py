from ..Cadastrar.criarConexao import criarConexao, database

def editarTurma(turma_antiga, turma_nova, icone_url):
    conn = criarConexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE turmas SET pk_nome_turma = %s, icone_url = %s WHERE pk_nome_turma = %s",
        (turma_nova, icone_url, turma_antiga)
    )
    conn.commit()
    conn.close()