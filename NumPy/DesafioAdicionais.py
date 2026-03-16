import numpy as np

def criar_vetor():
    vetor = np.arange(0,10)
    print(f'Vetor criado de 0 a 9: {vetor}')
    return vetor
    
def criar_array_boleano():
    arr = np.ones((3,3), dtype=bool)
    print(f'Array booleano 3x3:\n{arr}')

def impares():
    arr = criar_vetor()
    impares = arr[arr % 2 != 0]
    return impares
    
def substituir_valores():
    arr = criar_vetor()
    arr[arr % 2 != 0] = -1
    print(f'Vetor com valores impares substituídos por -1: {arr}')

def matriz_aleatoria():
    matriz = np.random.randint( 1, 100, size = (5,5))
    print(f'Matriz alearia 2x2 com valores entre 1 e 100 \n {matriz}')
    return matriz

def soma_coluna():
    matriz = matriz_aleatoria()
    soma = matriz.sum(axis=0)
    print(f'Soma dos valores de cada coluna: {soma}')

def valor_maximo():
    matriz = matriz_aleatoria()
    maximo = matriz.max(axis=1)
    print(f'Valor máximo da matriz por linha: {maximo}')
    
def broadcasting():
    vetor = np.arange(1,6)
    print(f'Vetor original: {vetor}')
    vetor = vetor + 2
    print(f'Vetor após aplicação de broadcasting (adicionando 2): {vetor}')

def concatenar():
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    concatenado = np.concatenate((arr1, arr2))
    print(f'Array concatenado: {concatenado}')
    
def inverter():
    arr = np.array([10,20,30,40])
    arr_invertido = arr[::-1]
    print(f'Array original: {arr}')
    print(f'Array invertido: {arr_invertido}')
    
