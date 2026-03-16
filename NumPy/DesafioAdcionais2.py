import numpy as np

def temperatura():
    arr = np.array([22, 24, 21, 23, 25, 20, 22])
    media = np.mean(arr)
    print(f"{media:.2f}°C")
    dia_quente = np.argmax(arr)
    print(f"Dia {dia_quente + 1}: {arr[dia_quente]}°C")

def valores_unicos():
    arr = np.array([1, 2, 2, 3, 4, 4, 4, 5])
    print(np.unique(arr))

def vendas_mensais():
    vendas = np.random.randint(50, 201, size=(3, 4))
    print(vendas.sum(axis=1))

def pontuacao_teste():
    pontuacoes = np.array([75, 88, 92, 65, 70, 80, 95, 60, 85, 78])
    print(f"Min: {pontuacoes.min()}, Max: {pontuacoes.max()}")

def sensores():
    sensores = np.random.rand(20)
    print(sensores[sensores > 0.7])

def precos_acoes():
    precos = np.array([120.50, 121.00, 119.80, 122.30, 120.00])
    variacao = (np.diff(precos) / precos[:-1]) * 100
    print(variacao)

def matriz_identidade():
    print(np.eye(4))

def zeros_e_uns():
    print(np.zeros((3, 3)))
    print(np.ones((2, 5)))

def redimensionar_imagem():
    print(np.random.rand(25).reshape((5, 5)))

def filtrar_pares():
    numeros = np.arange(10)
    print(numeros[numeros % 2 == 0])

def soma_acumulada():
    print(np.cumsum([1, 2, 3, 4, 5]))

def interpolacao_linear():
    print(np.linspace(0, 10, 5))

def media_ponderada():
    notas = np.array([80, 90, 70])
    pesos = np.array([0.3, 0.5, 0.2])
    print(np.average(notas, weights=pesos))

def transpor_dados():
    dados = np.array([[2, 4, 6], [70, 85, 90]])
    print(dados.T)

def inverter_eixos():
    matriz = np.arange(12).reshape(3, 4)
    print(np.flip(matriz, axis=0))

def comparar_arrays():
    a, b = np.array([1, 2, 3]), np.array([3, 2, 1])
    print(a == b)

def mascara_condicao():
    arr = np.random.randint(0, 101, 10)
    print(arr[arr > 50])

def contagem_valores():
    arr = np.array([1, 7, 3, 7, 5, 7])
    print(np.count_nonzero(arr == 7))

def arredondamento():
    print(np.round([1.23, 2.78, 3.50, 4.11]))

def combinar_arrays():
    arr1, arr2 = np.array([1, 2, 3]), np.array([4, 5, 6])
    print(np.vstack((arr1, arr2)))
