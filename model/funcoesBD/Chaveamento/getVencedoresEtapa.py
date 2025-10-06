from ..Cadastrar.criarConexao import criarConexao
import mysql.connector

def getVencedoresEtapa(esporte, classificacao, etapa):
    """
    Retorna a lista ordenada de IDs dos vencedores de uma etapa concluída.
    """
    conexao = criarConexao()
    if not conexao: return []
    
    # OBS: Usamos par_re1 e par_re2 para garantir a ordem correta na próxima rodada
    query = """
    SELECT pk_equipe_vencedora 
    FROM partidas
    WHERE fk_esporte = %s 
      AND fk_descricao = %s
      AND etapa = %s
      AND definida = 'sim'
    ORDER BY par_re1 ASC, par_re2 ASC;
    """
    try:
        with conexao.cursor() as cursor:
            cursor.execute(query, (esporte, classificacao, etapa))
            # Retorna uma lista simples de IDs (tuplas de 1 elemento)
            vencedores = [row[0] for row in cursor.fetchall()]
            return vencedores
    except mysql.connector.Error as err:
        print(f"Erro ao buscar vencedores: {err}")
        return []
    finally:
        conexao.close()