from ..Cadastrar.criarConexao import criarConexao
import mysql.connector

def buscarPartidasParaGestao(esporte, classificacao):
    """
    Busca todas as partidas de uma chave (esporte/classificação)
    trazendo os nomes das equipes.
    """
    conexao = criarConexao()
    if not conexao: return []

    try:
        # Usamos dictionary=True para retornar como dicionários
        with conexao.cursor(dictionary=True) as cursor: 
            query = """
            SELECT 
                p.pk_partida, p.fk_esporte, p.fk_descricao, p.etapa, 
                p.fk_equipe_casa, p.fk_equipe_visitante, p.pk_equipe_vencedora,
                ec.nome_equipe AS nome_equipe_casa,
                ev.nome_equipe AS nome_equipe_visitante
            FROM partidas p
            JOIN equipes ec ON p.fk_equipe_casa = ec.pk_equipe
            JOIN equipes ev ON p.fk_equipe_visitante = ev.pk_equipe
            WHERE p.fk_esporte = %s AND p.fk_descricao = %s
            ORDER BY p.etapa ASC, p.pk_partida ASC;
            """
            # Filtra pelo esporte E classificação, e traz todas as etapas
            cursor.execute(query, (esporte, classificacao)) 
            return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro ao buscar partidas para gestão: {err}")
        return []
    finally:
        conexao.close()