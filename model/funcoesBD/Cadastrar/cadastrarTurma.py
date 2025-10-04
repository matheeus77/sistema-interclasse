from .criarConexao import criarConexao, database

def cadastrarTurma(pk_nome_turma, icone_url):
    conn = criarConexao()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO turmas (pk_nome_turma, icone_url) VALUES (%s, %s)",
        (pk_nome_turma, icone_url)
    )

    conn.commit()
    conn.close()