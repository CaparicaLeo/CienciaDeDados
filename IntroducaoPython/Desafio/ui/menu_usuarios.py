from models.Usuario import Usuario
import services.usuario_service as usuario_service
from ui.helpers import titulo, pausar, menu


OPCOES = {
    "1": "Listar usuários",
    "2": "Cadastrar usuário",
    "3": "Ver empréstimos de um usuário",
    "0": "Voltar",
}


def exibir(usuarios: dict):
    while True:
        titulo("GERENCIAR USUARIOS")
        op = menu(OPCOES)

        if op == "1":
            titulo("Usuários cadastrados")
            usuario_service.listar(usuarios)

        elif op == "2":
            try:
                u = Usuario(
                    id_usuario=input("  ID: ").strip(),
                    nome      =input("  Nome: ").strip(),
                    cpf       =input("  CPF: ").strip(),
                )
                usuario_service.cadastrar(usuarios, u)
                print("  [OK] Usuario cadastrado!")
            except ValueError as e:
                print(f"  [ERRO] {e}")

        elif op == "3":
            id_u = input("  ID do usuario: ").strip()
            u = usuario_service.buscar(usuarios, id_u)
            if u:
                titulo(f"Emprestimos - {u.get_nome()}")
                u.listar_emprestimos()
            else:
                print("  [ERRO] Usuario nao encontrado.")

        elif op == "0":
            break
        else:
            print("  [AVISO]  Opção inválida.")

        pausar()