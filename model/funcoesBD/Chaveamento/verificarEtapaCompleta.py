from ..Cadastrar.criarConexao import criarConexao

def verificarEtapaCompleta(esporte, classificacao, etapa):
    """
    Verifica se todas as partidas de uma etapa foram resolvidas.
    """
    conexao = criarConexao()
    if not conexao: return False
    
    query = """
    SELECT COUNT(*) 
    FROM partidas
    WHERE fk_esporte = %s 
      AND fk_descricao = %s
      AND etapa = %s
      AND definida = 'nao';
    """
    try:
        with conexao.cursor() as cursor:
            cursor.execute(query, (esporte, classificacao, etapa))
            # Se o COUNT for 0, a etapa está completa
            return cursor.fetchone()[0] == 0 
    except:
        return False
    finally:
        conexao.close()