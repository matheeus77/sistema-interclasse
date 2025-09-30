import mysql.connector

database = 'etemfl83_inter_classe'

def criarConexao():
    conexaoBD = mysql.connector.connect(
        host='br418.hostgator.com.br',
        user='etemfl83_interclasse',
        password='L=ky%HhV2E5W',
        database=database
    )
    return conexaoBD