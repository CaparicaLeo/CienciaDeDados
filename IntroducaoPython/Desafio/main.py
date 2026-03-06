import sys
import os

# Garante que o pacote seja encontrado ao rodar: python main.py
sys.path.insert(0, os.path.dirname(__file__))

from services import persistencia
from ui import menu_livros, menu_usuarios, menu_emprestimos
from ui.helpers import titulo, menu, linha


OPCOES = {
    "1": "Gerenciar Livros",
    "2": "Gerenciar Usuarios",
    "3": "Emprestimos & Devolucoes",
    "4": "Salvar dados",
    "0": "Sair",
}


def main():
    livros, usuarios = persistencia.carregar()

    while True:
        titulo("SISTEMA DE BIBLIOTECA")
        op = menu(OPCOES)

        if op == "1":
            menu_livros.exibir(livros)
        elif op == "2":
            menu_usuarios.exibir(usuarios)
        elif op == "3":
            menu_emprestimos.exibir(livros, usuarios)
        elif op == "4":
            persistencia.salvar(livros, usuarios)
        elif op == "0":
            resp = input("  Salvar antes de sair? (s/n): ").strip().lower()
            if resp == "s":
                persistencia.salvar(livros, usuarios)
            linha()
            print("  Ate logo!")
            linha()
            break
        else:
            print("  [AVISO]  Opção inválida.")


if __name__ == "__main__":
    main()