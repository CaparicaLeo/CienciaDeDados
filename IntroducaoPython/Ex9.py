produtos = []

class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
    
    def vender(self, quantidade):
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            return self.preco * quantidade
        else:
            raise ValueError("Quantidade em estoque insuficiente.")
    
    def reabastecer(self, quantidade):
        self.estoque += quantidade
    
    def exibir_informacoes(self):
        return f"Produto: {self.nome}, Preço: R${self.preco:.2f}, Estoque: {self.estoque}"
    
    
def menu():
    print("\n1. Vender produto")
    print("2. Reabastecer produto")
    print("3. Exibir informações do produto")
    print("4. Sair")
    
if __name__ == "__main__":
    produtos.append(Produto("Caneta", 1.50, 100))
    produto = produtos[0]  # pega o produto da lista

    while True:
        menu()
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            quantidade = int(input("Digite a quantidade a vender: "))
            try:
                valor_venda = produto.vender(quantidade)
                print(f"Venda realizada! Valor total: R${valor_venda:.2f}")
            except ValueError as e:
                print(e)
        
        elif escolha == "2":
            quantidade = int(input("Digite a quantidade a reabastecer: "))
            produto.reabastecer(quantidade)
            print("Produto reabastecido com sucesso!")
        
        elif escolha == "3":
            print(produto.exibir_informacoes())
        
        elif escolha == "4":
            print("Saindo do programa.")
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")