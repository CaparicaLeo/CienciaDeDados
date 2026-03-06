from services import emprestimo_service
from ui.helpers import titulo, pausar, menu


OPCOES = {
    "1": "Emprestar livro",
    "2": "Devolver livro",
    "0": "Voltar",
}


def exibir(livros: dict, usuarios: dict):
    while True:
        titulo("EMPRESTIMOS & DEVOLUCOES")
        op = menu(OPCOES)

        if op == "1":
            try:
                isbn  = input("  ISBN do livro: ").strip()
                id_u  = input("  ID do usuário: ").strip()
                dias  = input("  Prazo em dias [14]: ").strip()
                prazo = int(dias) if dias else 14
                emprestimo_service.emprestar(livros, usuarios, isbn, id_u, prazo)
                print("  [OK] Emprestimo realizado!")
            except (KeyError, PermissionError, ValueError) as e:
                print(f"  [ERRO] {e}")

        elif op == "2":
            try:
                isbn = input("  ISBN do livro: ").strip()
                id_u = input("  ID do usuário: ").strip()
                emprestimo_service.devolver(livros, usuarios, isbn, id_u)
                print("  [OK] Devolucao registrada!")
            except (KeyError, ValueError) as e:
                print(f"  [ERRO] {e}")

        elif op == "0":
            break
        else:
            print("  [AVISO]  Opção inválida.")

        pausar()