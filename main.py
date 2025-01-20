import math
import time
import os

def abrir_caminho():
    with open('tsp1_253.txt','r',encoding='utf-8') as caminho:
        linhas = caminho.readlines()
    caminhos = [list(map(int,linha.split())) for linha in linhas]    # Lê os valores do arquivo e preenche em uma lista de listas
    return caminhos

def inicializacao_bb():
    caminhos = abrir_caminho()
    caminhos_aux=caminhos      
    return caminhos

def calcular_distancia(x1,x2,y1,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)  # Calcula a distância entre dois pontos da matriz


os.system('cls')
caminho=inicializacao_bb()

while True:
    try:
        x_inicial=input("Digite o 'x' inicial da matriz ")
        x_inicial=int(x_inicial)
        y_inicial=input("Digite o 'y' inicial da matriz ")
        y_inicial=int(y_inicial)
        if x_inicial>(len(caminho[0])-1) or x_inicial<0 or y_inicial>(len(caminho)-1) or y_inicial<0:
            print('Posição fora do range')
        else:
            caminho[x_inicial][y_inicial]=-2
            break
    except ValueError:                                                        #Lê e verifica se a entrada é aceita
        print('Digite um número inteiro')
        time.sleep(2)
        os.system('cls')



for linha in caminho:
    print(linha)






