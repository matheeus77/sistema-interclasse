import math
import random
import mysql.connector

# IMPORTAÇÕES RELATIVAS CORRIGIDAS:

# 1. Importa a função de busca de equipes (assumindo que está em um arquivo irmão)
#    Se o arquivo for 'buscarEquipesPorModCla.py' na mesma pasta.
from .buscarEquipesPorModCla import buscarEquipesPorModCla

# 2. Importa a conexão (assumindo que está em funcoesBD/Cadastrar/criarConexao.py)
#    Sobe um nível (..) para 'funcoesBD', desce para 'Cadastrar' e pega 'criarConexao'
from ..Cadastrar.criarConexao import criarConexao, database 


def gerar_chaveamento_sem_bye_contra_bye(equipes_ids):
    """
    Gera um chaveamento de mata-mata com semeadura, garantindo que BYEs não se enfrentem.
    
    Args:
        equipes_ids (list): Uma lista de PKs (int) das equipes, JÁ ORDENADAS ou EMBARALHADAS
                            de acordo com a lógica de turmas/semeadura.
        
    Returns:
        list: Uma lista de listas, representando o chaveamento rodada por rodada.
    """
    n_equipes = len(equipes_ids)
    
    if n_equipes < 2:
        return []

    # Passo 1: Determinar o tamanho da chave e a quantidade de BYEs
    potencia_de_2 = 2 ** math.ceil(math.log2(n_equipes))
    n_byes = potencia_de_2 - n_equipes
    
    # As equipes que recebem BYE são as primeiras da lista
    equipes_com_bye = equipes_ids[:n_byes]
    equipes_sem_bye = equipes_ids[n_byes:]

    chaveamento_completo = []
    
    # Passo 2: Criar a primeira rodada com semeadura inversa (para equipes sem BYE)
    partidas_primeira_rodada = []
    
    n_partidas_sem_bye = len(equipes_sem_bye) // 2
    for i in range(n_partidas_sem_bye):
        equipe_1 = equipes_sem_bye[i]
        # Lógica de semeadura inversa: primeiro vs último, segundo vs penúltimo, etc.
        equipe_2 = equipes_sem_bye[len(equipes_sem_bye) - 1 - i]
        partidas_primeira_rodada.append([equipe_1, equipe_2])
    
    chaveamento_completo.append(partidas_primeira_rodada)
    
    # Passo 3: Simular as próximas rodadas
    # Combina BYEs (que avançam automaticamente) com placeholders para os vencedores da 1ª rodada
    rodada_atual = equipes_com_bye + [f"Vencedor da partida {i+1}" for i in range(len(partidas_primeira_rodada))]
    
    # Simula rodadas futuras (apenas para estruturar o chaveamento)
    while len(rodada_atual) > 1:
        partidas_rodada = []
        
        # Embaralha os participantes da rodada futura
        random.shuffle(rodada_atual)
        
        # Pareamento
        for i in range(0, len(rodada_atual), 2):
            partidas_rodada.append([rodada_atual[i], rodada_atual[i+1]])
        
        chaveamento_completo.append(partidas_rodada)
        
        # Prepara a lista de "vencedores" para a próxima rodada
        rodada_atual = [f"Vencedor da partida {i+1}" for i in range(len(partidas_rodada))]

    return chaveamento_completo


def salvar_partidas(chaveamento, esporte, classificacao):
    """Salva apenas as partidas da primeira rodada no banco de dados."""
    conexao = criarConexao()
    if not conexao:
        print("Erro: Não foi possível conectar ao banco de dados para salvar as partidas.")
        return 0
    
    cursor = conexao.cursor()
    partidas_inseridas = 0
    
    # Query para inserção na tabela 'partidas'
    query = """
    INSERT INTO partidas 
        (fk_esporte, fk_descricao, fk_equipe_casa, fk_equipe_visitante, 
         definida, par_re1, par_re2, etapa)
    VALUES 
        (%s, %s, %s, %s, 'nao', 0, 0, %s)
    """

    # O chaveamento é uma lista de rodadas. Só salvamos a primeira (índice 0)
    if chaveamento and chaveamento[0]:
        etapa_atual = 1 # Primeira rodada
        
        for partida in chaveamento[0]:
            equipe_casa = partida[0]
            equipe_visitante = partida[1]
            
            # Verificação para ignorar BYEs (que aparecem como strings 'Vencedor...')
            # Na primeira rodada, todas as entradas que são PKs (int) são partidas reais.
            if isinstance(equipe_casa, int) and isinstance(equipe_visitante, int):
                dados_partida = (
                    esporte, 
                    classificacao, 
                    equipe_casa, 
                    equipe_visitante, 
                    etapa_atual
                )
                try:
                    cursor.execute(query, dados_partida)
                    partidas_inseridas += 1
                except mysql.connector.Error as err:
                    print(f"Erro ao inserir partida no BD: {err}")
    
    conexao.commit()
    cursor.close()
    conexao.close()
    return partidas_inseridas


def gerarChaveamento(esporte, classificacao):
    
    print(f"--- Gerando Chaveamento para {esporte} ({classificacao}) ---")
    
    # 1. BUSCA AS EQUIPES E INFORMAÇÕES
    # A função buscarEquipesPorModCla deve retornar uma lista de dicionários
    equipes_db = buscarEquipesPorModCla(esporte, classificacao)
    
    if not equipes_db:
        print("Status: Falha. Não há equipes cadastradas ou erro de conexão/consulta.")
        return

    # Extrai o tipo de esporte
    tipo_grupo = equipes_db[0]['grupo'] if equipes_db and 'grupo' in equipes_db[0] else 'Coletivo'
    
    # 2. APLICA A REGRA DE CONFRONTO DE TURMAS
    equipes_para_chavear = []
    equipes_com_info = [{'id': eq['pk_equipe'], 'turma': eq['turma']} for eq in equipes_db]
    
    if tipo_grupo == 'Individual':
        print("Regra: Esporte Individual. Confronto entre turmas permitido.")
        
        # Embaralha todas as equipes, pois não há restrição
        equipes_para_chavear = [eq['id'] for eq in equipes_com_info]
        random.shuffle(equipes_para_chavear)
        
    else: # Esporte Coletivo
        print("Regra: Esporte Coletivo. Tentando evitar confrontos de mesma turma na 1ª Rodada.")
        
        # Agrupa equipes por turma
        turmas_agrupadas = {}
        for eq in equipes_com_info:
            # Garante que usamos a PK e a turma
            turmas_agrupadas.setdefault(eq['turma'], []).append(eq['id'])
            
        # Tenta criar uma lista onde as turmas se alternam para 'espalhar' as equipes
        todas_listas = list(turmas_agrupadas.values())
        
        # Pega uma equipe de cada turma em sequência (até que as listas acabem)
        while any(todas_listas):
            for lista_equipes in todas_listas:
                if lista_equipes:
                    # Usa .pop() para pegar o último ID e remover da lista
                    equipe_escolhida = lista_equipes.pop() 
                    equipes_para_chavear.append(equipe_escolhida)
        
        # Um embaralhamento final suave pode ser feito sem reorganizar muito
        # o que já foi espaçado, mas vamos manter o espalhamento simples por enquanto.


    # 3. GERA O CHAVEAMENTO
    chaveamento = gerar_chaveamento_sem_bye_contra_bye(equipes_para_chavear)
    
    # 4. SALVA NO BANCO DE DADOS
    partidas_salvas = salvar_partidas(chaveamento, esporte, classificacao)
    
    # 5. RELATÓRIO FINAL
    print("\n" + "="*50)
    print(f"CHAVEAMENTO {esporte} ({classificacao}) CONCLUÍDO.")
    print(f"Total de equipes: {len(equipes_db)}")
    print(f"Total de partidas da 1ª rodada salvas no BD: {partidas_salvas}")
    print("="*50 + "\n")
    
    # Imprime o chaveamento (para visualização no console)
    for i, rodada in enumerate(chaveamento):
        print(f"--- Etapa {i + 1} ---")
        for partida in rodada:
            # Partidas da 1ª rodada mostram o ID (int)
            # Partidas futuras mostram o placeholder (str)
            print(f"Partida {partida[0]} vs {partida[1]}")
            
    return chaveamento


# O ponto de execução principal para evitar o RuntimeWarning
if __name__ == "__main__":
    # EXEMPLO DE CHAMADA DE TESTE (Substitua por um esporte real do seu BD)
    # Certifique-se de que a função criarConexao() está funcionando!
    gerarChaveamento('Futsal', 'Masculino')
    # gerarChaveamento('Tênis de Mesa', 'Misto')