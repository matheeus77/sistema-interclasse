from .criarConexao import criarConexao, database

def buscarEstatisticasPorModalidade(modalidade=None):
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)
    if modalidade is None:
        cursor.execute(f'SELECT DISTINCT fk_esporte FROM {database}.estatisticas_esporte')
        esportesComEst = cursor.fetchall()
    
        return esportesComEst
    else:
        cursor.execute(f'SELECT * FROM {database}.estatisticas_esporte WHERE fk_esporte = %s', (modalidade,))

        estatisticasBuscadas = cursor.fetchall()

        return estatisticasBuscadas
    cursor.close()
    conexao.close()
     