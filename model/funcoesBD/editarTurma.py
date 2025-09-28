from .criarConexao import criarConexao, database

def editarTurma(turma_antiga, turma_nova):
    conn = criarConexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE turmas SET pk_nome_turma = %s WHERE pk_nome_turma = %s",
        (turma_nova, turma_antiga)
    )
    conn.commit()
    conn.close()