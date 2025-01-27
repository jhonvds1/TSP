

import math

def abrir_caminho(arquivo='tsp5_27603.txt'):
    """
    Lê um arquivo de texto contendo as distâncias do TSP e retorna uma matriz.
    """
    try:
        with open(arquivo, 'r', encoding='utf-8') as caminho:
            linhas = caminho.readlines()
        return [list(map(int, linha.split())) for linha in linhas]
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return []
    except ValueError:
        print("Erro: O arquivo contém dados inválidos.")
        return []

def encontrar_menor_caminho(caminhos, inicio):
    """
    Encontra o menor caminho partindo de um vértice inicial usando abordagem gulosa.
    """
    visitado = [False] * len(caminhos)
    visitado[inicio] = True
    caminho = [inicio]
    custo_total = 0
    atual = inicio

    for _ in range(len(caminhos) - 1):
        prox_vertice = -1
        dist_min = float('inf')

        for j, distancia in enumerate(caminhos[atual]):
            if not visitado[j] and distancia < dist_min:
                dist_min = distancia
                prox_vertice = j

        visitado[prox_vertice] = True
        caminho.append(prox_vertice)
        custo_total += dist_min
        atual = prox_vertice

    # Volta ao ponto inicial
    custo_total += caminhos[atual][inicio]
    caminho.append(inicio)

    return caminho, custo_total

def calcular_custo(caminhos, caminho):
    """
    Calcula o custo total de um caminho.
    """
    custo = 0
    for i in range(len(caminho) - 1):
        custo += caminhos[caminho[i]][caminho[i + 1]]
    return custo

def refinamento_2opt(caminhos, caminho):
    """
    Refina o caminho usando a técnica 2-opt.
    """
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(1, len(caminho) - 2):
            for j in range(i + 1, len(caminho) - 1):
                if j - i == 1:  # Evita troca adjacente
                    continue
                novo_caminho = caminho[:i] + caminho[i:j][::-1] + caminho[j:]
                if calcular_custo(caminhos, novo_caminho) < calcular_custo(caminhos, caminho):
                    caminho = novo_caminho
                    melhorou = True
    return caminho

def inicializacao_bb():
    """
    Encontra o melhor caminho e custo para o problema TSP com refinamento.
    """
    caminhos = abrir_caminho()
    if not caminhos:  # Verifica se os caminhos foram carregados corretamente
        return None, float('inf')

    melhor_caminho = None
    melhor_custo = float('inf')

    for inicio in range(len(caminhos)):
        caminho, custo = encontrar_menor_caminho(caminhos, inicio)
        caminho = refinamento_2opt(caminhos, caminho)  # Aplica refinamento
        custo = calcular_custo(caminhos, caminho)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_caminho = caminho

    return melhor_caminho, melhor_custo

# Execução principal
melhor_caminho, melhor_custo = inicializacao_bb()
if melhor_caminho:
    print(f"O melhor caminho e: {melhor_caminho} e o custo e: {melhor_custo}")
else:
    print("Nao foi possível calcular o melhor caminho.")
