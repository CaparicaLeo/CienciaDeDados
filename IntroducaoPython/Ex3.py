def calculate_media(notas):
    if len(notas) == 0:
        return 0
    return round(sum(notas) / len(notas), 2)

def bigger_nota(notas):
    if len(notas) == 0:
        return None
    return max(notas)

def smaller_nota(notas):
    if len(notas) == 0:
        return None
    return min(notas)

if __name__ == "__main__":
    notas = []
    while (entrada := input("Digite uma nota (ou 'sair' para finalizar): ")) != "sair":
        try:
            nota = float(entrada)
            if 0 <= nota <= 10:
                notas.append(nota)
            else:
                print("Nota inválida. Digite um valor entre 0 e 10.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número ou 'sair'.")
    print("Notas:", notas)
    print("Média:", calculate_media(notas))
    print("Maior nota:", bigger_nota(notas))
    print("Menor nota:", smaller_nota(notas))