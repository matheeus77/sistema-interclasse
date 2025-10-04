from ..Cadastrar.criarConexao import criarConexao

def buscarAlunosPorTurma(turma):
    conn = criarConexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT pk_matricula, nome_aluno, fk_nome_turma, fk_classificacao FROM alunos WHERE fk_nome_turma = %s",
        (turma,)
    )
    alunos = cursor.fetchall()  # retorna lista de tuplas
    conn.close()
    return alunos

