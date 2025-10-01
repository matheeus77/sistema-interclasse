from ..Cadastrar.criarConexao import criarConexao, database
from datetime import datetime

def buscarEventosCalendario(ano,mes):
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)

    eventos = []
    primeiroDia = f'{ano}-{mes:02d}-01'
    proximoMes = mes + 1
    proximoAno = ano
    if proximoMes > 12:
        proximoMes = 1
        proximoAno += 1
    ultimoDia = f'{proximoAno}-{proximoMes:02d}-01'
    cursor.execute("""
            SELECT c.dia_evento, p.fk_esporte, p.fk_equipe_casa, p.fk_equipe_visitante
            FROM calendario AS c JOIN partidas AS p ON c.fk_partida = p.pk_partida
            WHERE c.dia_evento >= %s AND c.dia_evento < %s
        """, (primeiroDia, ultimoDia))
    
    eventos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return eventos

buscarEventosCalendario(2025,8)

diaAtual = datetime.today()
ano = diaAtual.year
mes = diaAtual.month

print(diaAtual)
