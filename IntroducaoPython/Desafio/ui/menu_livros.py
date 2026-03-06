from models.Livro import Livro
from services import livro_service
from ui.helpers import titulo, pausar, menu


OPCOES = {
    "1": "Listar todos os livros",
    "2": "Buscar por título",
    "3": "Buscar por autor",
    "4": "Buscar por ISBN",
    "5": "Adicionar livro",
    "6": "Remover livro",
    "0": "Voltar",
}


def exibir(livros: dict):
    while True:
        titulo("GERENCIAR LIVROS")
        op = menu(OPCOES)

        if op == "1":
            titulo("Todos os livros")
            livro_service.listar(livros)

        elif op == "2":
            t = input("  Trecho do título: ")
            resultado = livro_service.buscar_por_titulo(livros, t)
            titulo(f"Resultados — '{t}'")
            [print(f"  {l}") for l in resultado] if resultado else print("  Nenhum encontrado.")

        elif op == "3":
            a = input("  Trecho do autor: ")
            resultado = livro_service.buscar_por_autor(livros, a)
            titulo(f"Resultados — '{a}'")
            [print(f"  {l}") for l in resultado] if resultado else print("  Nenhum encontrado.")

        elif op == "4":
            isbn = input("  ISBN: ")
            l = livro_service.buscar_por_isbn(livros, isbn)
            print(f"  {l}" if l else "  Livro não encontrado.")

        elif op == "5":
            try:
                livro = Livro(
                    id_livro=input("  ID: ").strip(),
                    titulo  =input("  Título: ").strip(),
                    autor   =input("  Autor: ").strip(),
                    isbn    =input("  ISBN: ").strip(),
                )
                livro_service.adicionar(livros, livro)
                print("  [OK] Livro adicionado!")
            except ValueError as e:
                print(f"  [ERRO] {e}")

        elif op == "6":
            isbn = input("  ISBN: ").strip()
            try:
                livro_service.remover(livros, isbn)
                print("  [OK] Livro removido.")
            except KeyError as e:
                print(f"  [ERRO] {e}")

        elif op == "0":
            break
        else:
            print("  [AVISO]  Opção inválida.")

        pausar()