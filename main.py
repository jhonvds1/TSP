import numpy as np
import heapq

# Função para abrir o arquivo e ler os dados
def abrir_caminho():
    with open('tsp5_27603.txt', 'r', encoding='utf-8') as caminho:
        linhas = caminho.readlines()
    caminhos = [list(map(int, linha.split())) for linha in linhas]
    return caminhos

# Função para calcular a distância euclidiana entre dois pontos
def distancia(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Função para implementar o Algoritmo do Vizinho Mais Próximo
def tsp_vizinho_mais_proximo(caminhos):
    # Extraindo os pontos (coordenadas) do arquivo
    pontos = [(linha[1], linha[2]) for linha in caminhos]
    
    # Inicializando a solução
    caminho = [0]  # Começa do ponto 0
    visitados = set(caminho)
    
    custo_total = 0
    atual = 0  # Ponto atual
    
    # Percorrendo os pontos para formar o caminho
    while len(caminho) < len(pontos):
        proximos_pontos = []
        for i in range(len(pontos)):
            if i not in visitados:
                dist = distancia(pontos[atual], pontos[i])
                proximos_pontos.append((dist, i))
        
        # Encontrando o ponto mais próximo
        proximo = min(proximos_pontos)[1]
        caminho.append(proximo)
        custo_total += min(proximos_pontos)[0]
        visitados.add(proximo)
        atual = proximo
    
    # Fechar o ciclo (voltar ao ponto inicial)
    custo_total += distancia(pontos[atual], pontos[caminho[0]])
    caminho.append(caminho[0])
    
    return caminho, custo_total

# Função principal
def main():
    caminhos = abrir_caminho()
    caminho, custo_total = tsp_vizinho_mais_proximo(caminhos)
    print("Caminho aproximado:", caminho)
    print("Custo total:", custo_total)

if __name__ == "__main__":
    main()
