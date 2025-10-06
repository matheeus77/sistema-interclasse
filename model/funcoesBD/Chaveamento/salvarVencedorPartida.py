from ..Cadastrar.criarConexao import criarConexao
import mysql.connector

def salvarVencedorPartida(partida_id, vencedor_id):
    """
    Registra o vencedor de uma partida e marca como 'sim' (definida).
    """
    conexao = criarConexao()
    if not conexao: return False

    try:
        with conexao.cursor() as cursor:
            query = """
            UPDATE partidas
            SET pk_equipe_vencedora = %s, definida = 'sim'
            WHERE pk_partida = %s AND definida = 'nao';
            """
            cursor.execute(query, (vencedor_id, partida_id))
            conexao.commit()
            return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Erro ao salvar vencedor: {err}")
        return False
    finally:
        conexao.close()