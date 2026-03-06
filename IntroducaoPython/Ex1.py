class Pessoa:
    def __init__(self, nome, idade, altura, cidade):
        self.nome = nome
        self.idade = idade
        self.altura = altura
        self.cidade = cidade

def insert_data(nome, idade, altura, cidade):
    pessoa = Pessoa(nome, idade, altura, cidade)
    return pessoa

def print_data(pessoa):
    print(f"{pessoa.nome} tem {pessoa.idade} anos, mede {pessoa.altura} metros e mora em {pessoa.cidade}.")

def main():
    nome = str(input("Digite o nome da pessoa: "))
    idade = int(input("Digite a idade da pessoa: "))
    altura = float(input("Digite a altura da pessoa (em metros): "))
    cidade = str(input("Digite a cidade onde a pessoa mora: "))

    pessoa = insert_data(nome, idade, altura, cidade)
    print_data(pessoa)

main()