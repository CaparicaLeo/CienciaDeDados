dicionario = {}

def estatisticas(*numeros):
    if len(numeros) == 0:
        return {}

    return {
        "media": sum(numeros) / len(numeros),
        "maximo": max(numeros),
        "minimo": min(numeros)
    }

if __name__ == "__main__":
    notas = []

    while (entrada := input("Digite uma nota (ou 'sair' para finalizar): ")) != "sair":
        notas.append(float(entrada))

    resultado = estatisticas(*notas)
    print(resultado)