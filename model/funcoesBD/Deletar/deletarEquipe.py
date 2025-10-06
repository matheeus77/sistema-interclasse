from ..Cadastrar.criarConexao import criarConexao, database
import mysql.connector

def deletarEquipe(id):
    conexao = criarConexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM equipes WHERE pk_equipe = %s", (id,))
            conexao.commit()
        return "OK"  # <-- resposta simples pro fetch()
    except mysql.connector.IntegrityError as e:
        if "foreign key constraint" in str(e).lower():
            return "FK_ERROR"
        else:
            return "OTHER_ERROR"
    finally:
        conexao.close()

