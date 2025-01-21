def abrir_caminho():
    with open('tsp1_253.txt','r',encoding='utf-8') as caminho:
        linhas = caminho.readlines()
    caminhos = [list(map(int,linha.split())) for linha in linhas]    # Lê os valores do arquivo e preenche em uma lista de listas
    return caminhos

def inicializacao_bb():
    caminhos = abrir_caminho()     
    melhor_caminho=None
    melhor_custo=float('inf')
    for comeco in range(len(caminhos)):
        visitado = [False]*len(caminhos)
        visitado[comeco]=True
        caminho=[comeco]
        custo_total=0
        atual = comeco

        for _ in range(len(caminhos)-1):
            prox_vertice = -1
            dist_min=float('inf')
            
            for j in range(len(caminhos)):
                if not visitado[j]:
                    dist=caminhos[atual][j]
                    if dist < dist_min:
                        dist_min=dist
                        prox_vertice=j
            visitado[prox_vertice]=True
            caminho.append(prox_vertice)
            custo_total+=dist_min
            atual=prox_vertice
        
        custo_total+=caminhos[atual][comeco]
        caminho.append(comeco)
        if custo_total < melhor_custo:
            melhor_custo=custo_total
            melhor_caminho=caminho
    return melhor_caminho, melhor_custo




melhor_caminho,melhor_custo=inicializacao_bb()
print(f"o melhor caminho é: {melhor_caminho} e o melhor custo é: {melhor_custo}")
