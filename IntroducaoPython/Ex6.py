from math import dist

def calcular_distancia(p1, p2):
    return dist(p1, p2)

if __name__ == "__main__":
    x = float(input("Digite a coordenada x do primeiro ponto: "))
    y = float(input("Digite a coordenada y do primeiro ponto: "))
    x2 = float(input("Digite a coordenada x do segundo ponto: "))
    y2 = float(input("Digite a coordenada y do segundo ponto: "))
    
    ponto1 = (x, y)
    ponto2 = (x2, y2)
    distancia = calcular_distancia(ponto1, ponto2)
    print(f"A distância entre os pontos {ponto1} e {ponto2} é: {distancia:.2f}")