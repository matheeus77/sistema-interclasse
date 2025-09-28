from .criarConexao import criarConexao, database

def cadastrarTurma(pk_nome_turma):
    conn = criarConexao()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO turmas (pk_nome_turma) VALUES (%s)", (pk_nome_turma,))
    
    conn.commit()
    conn.close()
