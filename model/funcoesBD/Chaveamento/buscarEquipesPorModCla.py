from ..Cadastrar.criarConexao import criarConexao, database
# Certifique-se de que a query executa com os parâmetros (esporte, classificacao)

def buscarEquipesPorModCla(esporte, classificacao):
    conexao = criarConexao()
    try:
        with conexao.cursor(dictionary=True) as cursor: # Adicione 'dictionary=True' para facilitar a manipulação
            query = """
                SELECT 
                    e.pk_equipe,
                    s.pk_esporte AS esporte,
                    t.pk_nome_turma AS turma,
                    c.pk_descricao AS classificacao,
                    e.nome_equipe,
                    s.grupo,          -- NOVO: Adicionamos o campo 'grupo'
                    s.qtd_jogadores   -- NOVO: Adicionamos a quantidade de jogadores
                FROM equipes e
                JOIN esportes s ON e.fk_esporte = s.pk_esporte
                JOIN turmas t ON e.fk_nome_turma = t.pk_nome_turma
                JOIN classificacao c ON e.fk_descricao = c.pk_descricao
                WHERE s.pk_esporte = %s AND c.pk_descricao = %s
            """
            # Certifique-se de passar os parâmetros corretos para o cursor
            cursor.execute(query, (esporte, classificacao)) 
            return cursor.fetchall()
    finally:
        conexao.close()