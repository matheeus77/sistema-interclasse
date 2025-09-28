from .criarConexao import criarConexao, database

def deletarTurma(turma):
    conn = criarConexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turmas WHERE pk_nome_turma = %s", (turma,))
    conn.commit()
    conn.close()