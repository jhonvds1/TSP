with open('tsp1_253.txt','r',encoding='utf-8') as caminho:
    linhas = caminho.readlines()
caminhos = [list(map(int,linha.split())) for linha in linhas]



