from .criarConexao import criarConexao

def buscarAlunosPorTurma(turma):
    conn = criarConexao()
    cursor = conn.cursor()
    cursor.execute("SELECT pk_matricula, nome_aluno FROM alunos WHERE fk_nome_turma = %s", (turma,))
    alunos = cursor.fetchall()  # retorna lista de tuplas
    conn.close()
    return alunos
