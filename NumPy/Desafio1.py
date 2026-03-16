import numpy as np

def gerar_dados():
    return np.random.randint(100, 500, size=12)

def processar_vendas(arr):
    # Transforma em 3x4
    return arr.reshape(3, 4)

def calcular_totais(matriz):
    print("Venda total por semana:", matriz.sum(axis=1))

def calcular_medias(matriz):
    print("Média de Vendas para cada dia da semana:", matriz.mean(axis=0))

def filtrar_vendas(matriz, limite=400):
    print(f"Dias com vendas acima de {limite}:", matriz[matriz > limite])

# O seu ponto de entrada (Main) gerencia o fluxo
if __name__ == "__main__":
    dados = gerar_dados()
    print("Array original:", dados)
    
    matriz_vendas = processar_vendas(dados)
    print("Array reshaped (3x4):\n", matriz_vendas)
    
    calcular_totais(matriz_vendas)
    calcular_medias(matriz_vendas)
    filtrar_vendas(matriz_vendas)