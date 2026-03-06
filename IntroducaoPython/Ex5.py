agenda_de_contatos = {
    "João": "123456789",
    "Maria": "987654321",
}
def adicionar_contato(nome, telefone):
    if nome in agenda_de_contatos:
        print(f"Contato '{nome}' já existe na agenda.")
    else:
        agenda_de_contatos[nome] = telefone
        print(f"Contato '{nome}' adicionado com sucesso.")

def buscar_contato(nome):
    return agenda_de_contatos.get(nome, "Contato não encontrado.")

def remover_contato(nome):
    del agenda_de_contatos[nome]
    print(f"Contato '{nome}' removido com sucesso.")
    
def listar_contatos():
    return agenda_de_contatos
    
def menu():
    while True:
        print("\nMenu:")
        print("1. Adicionar contato")
        print("2. Buscar contato")
        print("3. Remover contato")
        print("4. Listar contatos")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            nome = input("Digite o nome do contato: ")
            telefone = input("Digite o telefone do contato: ")
            adicionar_contato(nome, telefone)
        elif escolha == "2":
            nome = input("Digite o nome do contato para buscar: ")
            resultado = buscar_contato(nome)
            print(resultado)
        elif escolha == "3":
            nome = input("Digite o nome do contato para remover: ")
            remover_contato(nome)
        elif escolha == "4":
            contatos = listar_contatos()
            for nome, telefone in contatos.items():
                print(f"{nome}: {telefone}")
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
    