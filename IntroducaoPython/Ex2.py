import random as rnd

def generate_random_integer():
    return rnd.randint(1,10)

if __name__ == "__main__":
    numeros = [generate_random_integer() for _ in range(5)]
    print("Números gerados:", numeros)
    for numero in range(0,2):
        numeros.append(generate_random_integer())
    print("Números gerados após adição:", numeros)
    numeros.pop(generate_random_integer())
    print("Números gerados após remoção:", numeros)
    numeros.sort()
    print("Números gerados após ordenação:", numeros)
    