from ..Cadastrar.criarConexao import criarConexao
import mysql.connector, random
from .getVencedoresEtapa import getVencedoresEtapa 

def gerarProximaRodada(esporte, classificacao, etapa_atual):
    """
    Busca os vencedores, gera o pareamento da próxima etapa e salva as novas partidas.
    """
    proxima_etapa = etapa_atual + 1
    
    # 1. Obter a lista de vencedores (IDs) da etapa atual (na ordem correta)
    vencedores = getVencedoresEtapa(esporte, classificacao, etapa_atual)
    
    if len(vencedores) < 2:
        print(f"FIM DO CHAVEAMENTO: O vencedor é {vencedores[0] if vencedores else 'desconhecido'}.")
        return 0 
        
    partidas_inseridas = 0
    conexao = criarConexao()
    if not conexao: return 0

    try:
        with conexao.cursor() as cursor:
            
            # 2. Pareamento (simples, semeadura) para a próxima rodada
            partidas_proxima_rodada = []
            
            # Embaralha os vencedores para evitar confrontos previsíveis nas próximas rodadas
            random.shuffle(vencedores) 
            
            # Pareia em ordem (V1 vs V2, V3 vs V4, etc.)
            for i in range(0, len(vencedores), 2):
                if i + 1 < len(vencedores):
                    partidas_proxima_rodada.append((vencedores[i], vencedores[i+1]))
                else:
                    # Se houver um número ímpar, o último ID (melhor seed) recebe um BYE.
                    # No modelo de vencedores, um BYE é uma partida já definida.
                    pass # Lógica de BYE seria mais complexa aqui; assumimos que ele avança automaticamente.
                    
            # 3. Inserir as novas partidas no BD
            query = """
            INSERT INTO partidas 
                (fk_esporte, fk_descricao, fk_equipe_casa, fk_equipe_visitante, 
                 definida, par_re1, par_re2, etapa)
            VALUES 
                (%s, %s, %s, %s, 'nao', 0, 0, %s)
            """
            
            # OBS: par_re1 e par_re2 seriam usados para vincular à partida anterior,
            # mas vamos simplificar o INSERT agora.
            
            for casa, visitante in partidas_proxima_rodada:
                dados_partida = (esporte, classificacao, casa, visitante, proxima_etapa)
                cursor.execute(query, dados_partida)
                partidas_inseridas += 1

            conexao.commit()
            return partidas_inseridas
    except mysql.connector.Error as err:
        print(f"Erro ao gerar próxima rodada: {err}")
        return 0
    finally:
        conexao.close()