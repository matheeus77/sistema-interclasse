import math

def gerar_chaveamento_sem_bye_contra_bye(equipes):
    """
    Gera um chaveamento de mata-mata com semeadura inversa,
    garantindo que BYEs não se enfrentem.
    
    Args:
        equipes (list): Uma lista de nomes de equipes.
        
    Returns:
        list: Uma lista de listas, onde cada lista interna representa uma rodada
              e contém as partidas daquela rodada.
    """
    n_equipes = len(equipes)
    
    if n_equipes < 2:
        return []

    # Passo 1: Determinar o tamanho da chave e a quantidade de BYEs
    potencia_de_2 = 2 ** math.ceil(math.log2(n_equipes))
    n_byes = potencia_de_2 - n_equipes
    
    # Passo 2: Preparar a lista de participantes
    # Opcional: Embaralhar para evitar semeadura fixa
    import random
    random.shuffle(equipes)
    
    # As equipes que recebem BYE são as melhores "sementes" (as primeiras da lista)
    equipes_com_bye = equipes[:n_byes]
    equipes_sem_bye = equipes[n_byes:]

    chaveamento_completo = []
    
    # Passo 3: Criar a primeira rodada com semeadura inversa
    partidas_primeira_rodada = []
    
    # Parear equipes sem BYE
    n_partidas_sem_bye = len(equipes_sem_bye) // 2
    for i in range(n_partidas_sem_bye):
        equipe_1 = equipes_sem_bye[i]
        equipe_2 = equipes_sem_bye[n_partidas_sem_bye * 2 - 1 - i]
        partidas_primeira_rodada.append([equipe_1, equipe_2])
    
    chaveamento_completo.append(partidas_primeira_rodada)
    
    # Passo 4: Simular as próximas rodadas
    rodada_atual = equipes_com_bye + [f"Vencedor da partida {i+1}" for i in range(len(partidas_primeira_rodada))]
    
    while len(rodada_atual) > 1:
        partidas_rodada = []
        # Embaralha as equipes da rodada para evitar confronto fixo
        random.shuffle(rodada_atual)
        for i in range(0, len(rodada_atual), 2):
            partidas_rodada.append([rodada_atual[i], rodada_atual[i+1]])
        
        chaveamento_completo.append(partidas_rodada)
        
        rodada_atual = [f"Vencedor da partida {i+1}" for i in range(len(partidas_rodada))]

    return chaveamento_completo

def gerarChaveamento(esporte, classificacao):
    # Simulação dos dados, substitua pela sua função de busca
    equipes_db = [{'pk_equipe': f'Equipe {i+1}'} for i in range(12)] # Exemplo com 7 equipes
    lista_equipe = [eq['pk_equipe'] for eq in equipes_db]
    
    chaveamento = gerar_chaveamento_sem_bye_contra_bye(lista_equipe)
    
    # Imprime o chaveamento gerado
    for i, rodada in enumerate(chaveamento):
        print(f"--- Etapa {i + 1} ---")
        for partida in rodada:
            print(f"Partida {partida[0]} vs {partida[1]}")
            
# Chamando a função para teste
gerarChaveamento('tes','mas')
