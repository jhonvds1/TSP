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
