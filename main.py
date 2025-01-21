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










import numpy as np

# Função para abrir o arquivo e ler os dados
def abrir_caminho():
    with open('tsp5_27603.txt', 'r', encoding='utf-8') as caminho:
        linhas = caminho.readlines()
    caminhos = [list(map(int, linha.split())) for linha in linhas]
    return caminhos

# Função para calcular a distância euclidiana entre dois pontos
def distancia(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Função para gerar a matriz de distâncias
def gerar_matriz_distancias(pontos):
    n = len(pontos)
    matriz_distancias = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia(pontos[i], pontos[j])
            matriz_distancias[i][j] = d
            matriz_distancias[j][i] = d
    return matriz_distancias

# Função para calcular o custo de um caminho
def calcular_custo(caminho, matriz_distancias):
    custo = 0
    for i in range(len(caminho) - 1):
        custo += matriz_distancias[caminho[i]][caminho[i + 1]]
    custo += matriz_distancias[caminho[-1]][caminho[0]]  # Fechar o ciclo
    return custo

# Função para implementar o Algoritmo do Vizinho Mais Próximo
def tsp_vizinho_mais_proximo(caminhos):
    pontos = [(linha[1], linha[2]) for linha in caminhos]
    matriz_distancias = gerar_matriz_distancias(pontos)
    
    melhor_caminho = None
    menor_custo = float('inf')
    
    # Tentar diferentes pontos de partida
    for ponto_inicial in range(len(pontos)):
        caminho = [ponto_inicial]
        visitados = set(caminho)
        custo_total = 0
        atual = ponto_inicial
        
        while len(caminho) < len(pontos):
            proximos_pontos = []
            for i in range(len(pontos)):
                if i not in visitados:
                    dist = matriz_distancias[atual][i]
                    proximos_pontos.append((dist, i))
            
            proximo = min(proximos_pontos)[1]
            caminho.append(proximo)
            custo_total += min(proximos_pontos)[0]
            visitados.add(proximo)
            atual = proximo
        
        # Fechar o ciclo
        custo_total += matriz_distancias[atual][caminho[0]]
        
        if custo_total < menor_custo:
            melhor_caminho = caminho
            menor_custo = custo_total

    # Aplicar 2-opt para otimizar o caminho
    melhor_caminho, menor_custo = two_opt(melhor_caminho, pontos, matriz_distancias)
    
    return melhor_caminho, menor_custo

# Função 2-opt para melhorar a solução
def two_opt(caminho, pontos, matriz_distancias):
    melhor_caminho = caminho
    melhor_custo = calcular_custo(melhor_caminho, matriz_distancias)
    
    for i in range(1, len(caminho) - 2):
        for j in range(i + 1, len(caminho)):
            if j - i == 1: continue  # Ignora vizinhos imediatos
            novo_caminho = melhor_caminho[:]
            novo_caminho[i:j] = reversed(melhor_caminho[i:j])
            novo_custo = calcular_custo(novo_caminho, matriz_distancias)
            
            if novo_custo < melhor_custo:
                melhor_caminho = novo_caminho
                melhor_custo = novo_custo

    return melhor_caminho, melhor_custo

# Função principal
def main():
    caminhos = abrir_caminho()
    melhor_caminho, custo_total = tsp_vizinho_mais_proximo(caminhos)
    print("Caminho aproximado:", melhor_caminho)
    print("Custo total:", custo_total)

if __name__ == "__main__":
    main()
