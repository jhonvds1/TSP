import numpy as np

def abrir_caminho():
    with open('tsp3_1194.txt', 'r', encoding='utf-8') as caminho:
        linhas = caminho.readlines()
    caminhos = [list(map(int, linha.split())) for linha in linhas]
    return caminhos

def reduzir_matriz(matriz):
    # Reduz a matriz de custos e retorna a matriz reduzida e o custo da redução.
    custo_reducao = 0
    
    # Reduz as linhas
    for i in range(len(matriz)):
        min_linha = min(matriz[i]) 
        if min_linha < float('inf'):
            custo_reducao += min_linha
            for j in range(len(matriz)):
                matriz[i][j] -= min_linha
    
    # Reduz as colunas
    for j in range(len(matriz)):
        min_coluna = min(matriz[i][j] for i in range(len(matriz)))
        if min_coluna < float('inf'):
            custo_reducao += min_coluna
            for i in range(len(matriz)):
                matriz[i][j] -= min_coluna
    
    return matriz, custo_reducao

def tsp_branch_and_bound(matriz):
    n = len(matriz)
    melhor_caminho = None
    melhor_custo = float('inf')

    def bnb_recursivo(cidade_atual, visitados, custo_atual, caminho):
        nonlocal melhor_caminho, melhor_custo

        # Se todas as cidades foram visitadas, retorna à inicial
        if len(caminho) == n:
            custo_total = custo_atual + matriz[cidade_atual][caminho[0]]
            if custo_total < melhor_custo:
                melhor_custo = custo_total
                melhor_caminho = caminho + [caminho[0]]
            return

        # Tenta todas as cidades não visitadas
        for prox_cidade in range(n):
            if not visitados[prox_cidade] and matriz[cidade_atual][prox_cidade] < float('inf'):
                # Atualiza o custo parcial
                custo_parcial = custo_atual + matriz[cidade_atual][prox_cidade]

                # Poda: Se o custo parcial já for maior que o melhor custo, ignora
                if custo_parcial >= melhor_custo:
                    continue

                # Marca como visitada e avança para a próxima cidade
                visitados[prox_cidade] = True
                bnb_recursivo(prox_cidade, visitados, custo_parcial, caminho + [prox_cidade])
                visitados[prox_cidade] = False  # Backtracking

    # Cria uma cópia da matriz para preservá-la
    matriz_copy = np.array(matriz, dtype=float).tolist()

    # Inicializa a matriz reduzida
    matriz_reduzida, custo_inicial = reduzir_matriz(matriz_copy)
    
    # Começa o Branch and Bound a partir de cada cidade
    for inicio in range(n):
        visitados = [False] * n
        visitados[inicio] = True
        bnb_recursivo(inicio, visitados, custo_inicial, [inicio])

    return melhor_caminho, melhor_custo


# Executando o TSP com Branch and Bound
caminhos = abrir_caminho()
melhor_caminho, melhor_custo = tsp_branch_and_bound(caminhos)
print(f"O melhor caminho é: {melhor_caminho} com custo: {melhor_custo}")










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
    print(f"O melhor caminho é: {melhor_caminho} e o custo é: {melhor_custo}")
else:
    print("Não foi possível calcular o melhor caminho.")
