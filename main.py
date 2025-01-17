def abrir_caminho():
    with open('tsp1_253.txt','r',encoding='utf-8') as caminho:
        linhas = caminho.readlines()
    caminhos = [list(map(int,linha.split())) for linha in linhas]
    return caminhos

def inicializacao_bb():
    caminhos = abrir_caminho()
    caminhos_aux=caminhos
    

inicializacao_bb()


