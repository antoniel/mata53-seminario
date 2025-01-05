import math
import random
from copy import deepcopy

# ====================================================
#                 PARTE 1: LEITURA DO INPUT
# ====================================================
def ler_input(filepath):
    try:
        with open(filepath, 'r') as f:
            # Ignora linhas em branco e lê a primeira linha com dados
            primeira_linha = ''
            while not primeira_linha:
                primeira_linha = f.readline().strip()
            
            n, m, capacidade = map(int, primeira_linha.split())

            # Ignora linha em branco antes da matriz de distância
            f.readline()  # pula linha em branco

            # Ler dist_matrix (n x n)
            dist_matrix = []
            for _ in range(n):
                linha = f.readline().strip()
                if not linha:
                    raise ValueError(f"Erro ao ler matriz de distância na linha {_+2}")
                row = list(map(int, linha.split()))
                if len(row) != n:
                    raise ValueError(f"Número incorreto de colunas na matriz de distância, linha {_+2}")
                dist_matrix.append(row)

            # Ignora linha em branco antes da matriz de tempo
            f.readline()  # pula linha em branco

            # Ler time_matrix (n x n)
            time_matrix = []
            for _ in range(n):
                linha = f.readline().strip()
                if not linha:
                    raise ValueError(f"Erro ao ler matriz de tempo na linha {_+2+n}")
                row = list(map(int, linha.split()))
                if len(row) != n:
                    raise ValueError(f"Número incorreto de colunas na matriz de tempo, linha {_+2+n}")
                time_matrix.append(row)

            # Ignora linha em branco antes das tarefas
            f.readline()  # pula linha em branco

            # Ler m tarefas
            tasks = []
            for t_id in range(m):
                linha = f.readline().strip()
                if not linha:
                    raise ValueError(f"Erro ao ler tarefa {t_id+1}")
                    
                valores = linha.split()
                if len(valores) < 6:
                    raise ValueError(f"Dados insuficientes para tarefa {t_id+1}. Formato esperado: origem destino e1 l1 e2 l2")
                
                o, d = int(valores[0]), int(valores[1])
                e1, l1, e2, l2 = map(int, valores[2:6])
                
                # Calcula bônus dinâmico
                bonus_o, bonus_d = calcular_bonus_dinamico(o, d, dist_matrix, time_matrix)
                
                tasks.append({
                    'id': t_id,
                    'origem': o,
                    'destino': d,
                    'pickup_earliest': e1,
                    'pickup_latest': l1,
                    'dropoff_earliest': e2,
                    'dropoff_latest': l2,
                    'bonus_origem': bonus_o,
                    'bonus_destino': bonus_d
                })

            # Ignora linha em branco antes das coordenadas
            f.readline()  # pula linha em branco

            # Ler coords (opcional)
            coords = []
            for _ in range(n):
                linha = f.readline().strip()
                if not linha:
                    break
                x, y = map(int, linha.split())
                coords.append((x, y))

            return n, m, capacidade, dist_matrix, time_matrix, tasks, coords
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado")
        raise
    except ValueError as e:
        print(f"Erro no formato do arquivo: {str(e)}")
        raise
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        raise

# ====================================================
#                 PARTE 2: FUNÇÕES DE CUSTO
# ====================================================

def calcular_custo_rota(rota, dist_matrix):
    """ Distância total de uma rota. """
    if len(rota) < 2:
        return 0
    dist_total = 0
    for i in range(len(rota) - 1):
        dist_total += dist_matrix[rota[i]][rota[i+1]]
    return dist_total

def verificar_viabilidade(rota, tasks_incluidas, time_matrix, tasks, capacidade):
    """
    Exemplo simples de verificação de viabilidade:
      - Número de tarefas não excede capacidade
      - (Opcional) Verifica janelas triviais: e1 <= l1
    """
    if len(tasks_incluidas) > capacidade:
        return False
    for t_id in tasks_incluidas:
        if tasks[t_id]['pickup_earliest'] > tasks[t_id]['pickup_latest']:
            return False
    return True

def calcular_funcao_objetivo(rota, tasks_incluidas, dist_matrix, tasks):
    """
    FO = Distância total - (bonus_origem + bonus_destino de cada tarefa).
    """
    dist_total = calcular_custo_rota(rota, dist_matrix)
    bonus_total = 0
    for t_id in tasks_incluidas:
        bonus_total += (tasks[t_id]['bonus_origem'] + tasks[t_id]['bonus_destino'])
    return dist_total - bonus_total

# ====================================================
#  PARTE 3: FUNÇÃO PARA CALCULAR GANHO LÍQUIDO DE UMA TAREFA
# ====================================================

def calcular_ganho_liquido(task, dist_matrix):
    """
    Ganho líqu. = (bonus_origem + bonus_destino) - custo_insercao

    Aqui, custo_insercao = dist[o][d], como aproximação simples.
    """
    o = task['origem']
    d = task['destino']
    bonus_o = task['bonus_origem']
    bonus_d = task['bonus_destino']

    custo_inserir = dist_matrix[o][d]  # simplificado
    ganho = (bonus_o + bonus_d) - custo_inserir
    return ganho

# ====================================================
#  PARTE 4: CONSTRUÇÃO INICIAL COM BASE NO GANHO LÍQUIDO
# ====================================================

def construir_solucao_inicial(n, m, capacidade, dist_matrix, time_matrix, tasks, debug=False):
    """
    1) Começa com uma rota [0,1,2,...,n-1,0] (embaralhada no meio, se quiser).
    2) Calcula o ganho líquido de TODAS as tarefas.
    3) Ordena as tarefas pelo maior ganho e vai inserindo, se for viável,
       até esgotar a capacidade ou não houver mais tarefas vantajosas.
    """

    # Exemplo de rota: [0,1,2, ..., n-1, 0]
    nos_intermediarios = list(range(1, n))
    random.shuffle(nos_intermediarios)
    rota_inicial = [0] + nos_intermediarios + [0]

    # Calcula ganho líquido de cada tarefa
    lista_ganhos = []
    for t in tasks:
        g = calcular_ganho_liquido(t, dist_matrix)
        lista_ganhos.append((t['id'], g))

    # Ordena por G decrescente
    lista_ganhos.sort(key=lambda x: x[1], reverse=True)

    tasks_incluidas = []
    # Tenta inserir as tarefas com maior ganho primeiro
    for (t_id, g) in lista_ganhos:
        # Para inserir a tarefa, checa viabilidade
        teste_incluir = tasks_incluidas + [t_id]
        if verificar_viabilidade(rota_inicial, teste_incluir, time_matrix, tasks, capacidade):
            tasks_incluidas.append(t_id)

    if debug:
        print("[CONSTRUÇÃO - Ganho Líquido]")
        print("Rota inicial =", rota_inicial)
        print("Tasks incluídas =", tasks_incluidas)

    return rota_inicial, tasks_incluidas

# ====================================================
#   PARTE 5: EXEMPLO DE BUSCA LOCAL (OPCIONAL)
# ====================================================
def busca_local(rota, tasks_incluidas, dist_matrix, time_matrix, tasks, capacidade, max_iter=30, debug=False):
    """
    Exemplo simples de busca local:
    - Tenta remover / trocar tasks para ver se melhora FO
    - Mantém a mesma rota (não insere nós novos).
    """
    def fo(r, t):
        return calcular_funcao_objetivo(r, t, dist_matrix, tasks)

    best_fo = fo(rota, tasks_incluidas)
    best_rota = rota[:]
    best_tasks = tasks_incluidas[:]

    for _ in range(max_iter):
        op = random.choice(["remove", "swap"])
        if op == "remove" and best_tasks:
            t_remove = random.choice(best_tasks)
            nova = [x for x in best_tasks if x != t_remove]
            if verificar_viabilidade(best_rota, nova, time_matrix, tasks, capacidade):
                fo_nova = fo(best_rota, nova)
                if fo_nova < best_fo:
                    best_fo = fo_nova
                    best_tasks = nova[:]
                    if debug:
                        print("[BL] Removeu task", t_remove, "=> FO:", best_fo)
        elif op == "swap" and len(best_tasks) < capacidade:
            # Pegar 1 task da lista e 1 fora
            inside = best_tasks
            outside = [t['id'] for t in tasks if t['id'] not in inside]
            if inside and outside:
                t_remove = random.choice(inside)
                t_add = random.choice(outside)
                nova = [x for x in inside if x != t_remove]
                nova.append(t_add)
                if verificar_viabilidade(best_rota, nova, time_matrix, tasks, capacidade):
                    fo_nova = fo(best_rota, nova)
                    if fo_nova < best_fo:
                        best_fo = fo_nova
                        best_tasks = nova[:]
                        if debug:
                            print("[BL] Swap remove:", t_remove, "add:", t_add, "=> FO:", best_fo)

    return best_rota, best_tasks

def calcular_bonus_dinamico(origem, destino, dist_matrix, time_matrix):
    """
    Calcula bônus dinâmico baseado na distância e tempo da viagem
    Quanto maior a distância/tempo, maior o bônus para incentivar viagens longas
    """
    distancia = dist_matrix[origem][destino]
    tempo = time_matrix[origem][destino]
    
    # Fator de peso para distância e tempo
    peso_dist = 0.3
    peso_tempo = 0.2
    
    bonus_origem = int(distancia * peso_dist + tempo * peso_tempo)
    bonus_destino = int(bonus_origem * 0.7)  # Bônus de destino é 70% do bônus de origem
    
    return bonus_origem, bonus_destino

def mostrar_info_passageiros(tasks):
    print("\n=== INFORMAÇÕES DOS PASSAGEIROS ===")
    print(f"{'ID':^4} | {'Origem':^6} | {'Destino':^7} | {'Bônus Origem':^12} | {'Bônus Destino':^13} | {'Total Bônus':^11}")
    print("-" * 65)
    
    for task in tasks:
        t_id = task['id']
        origem = task['origem']
        destino = task['destino']
        bonus_o = task['bonus_origem']
        bonus_d = task['bonus_destino']
        total_bonus = bonus_o + bonus_d
        
        print(f"{t_id:^4} | {origem:^6} | {destino:^7} | {bonus_o:^12} | {bonus_d:^13} | {total_bonus:^11}")

# ====================================================
#         PARTE 6: PROGRAMA PRINCIPAL (MAIN)
# ====================================================
def main(debug=False):
    # Ajuste conforme seu arquivo
    filepath = "instancias/n5c4.in"

    # 1) Ler dados
    n, m, capacidade, dist_matrix, time_matrix, tasks, coords = ler_input(filepath)
    
    # Mostrar informações dos passageiros
    mostrar_info_passageiros(tasks)

    # 2) Construir solução inicial com base no maior ganho líquido
    rota_ini, tasks_ini = construir_solucao_inicial(
        n, m, capacidade,
        dist_matrix, time_matrix,
        tasks,
        debug=debug
    )

    # 3) (Opcional) Busca local
    rota_final, tasks_final = busca_local(
        rota_ini,
        tasks_ini,
        dist_matrix,
        time_matrix,
        tasks,
        capacidade,
        max_iter=50,
        debug=debug
    )

    # 4) Resultado
    fo_final = calcular_funcao_objetivo(rota_final, tasks_final, dist_matrix, tasks)
    print("\n=== RESULTADO FINAL ===")
    print("Rota:", rota_final)
    print("Tasks incluídas:", tasks_final)
    print("Função Objetivo:", fo_final)

if __name__ == "__main__":
    main(debug=True)