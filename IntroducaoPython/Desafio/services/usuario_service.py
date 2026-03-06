from models.Usuario import Usuario

def cadastrar(usuarios: dict, usuario: Usuario):
    if usuario.get_id() in usuarios:
        raise ValueError(f"Usuário com ID '{usuario.get_id()}' já cadastrado.")
    usuarios[usuario.get_id()] = usuario


def buscar(usuarios: dict, id_usuario: str) -> Usuario | None:
    return usuarios.get(id_usuario)


def listar(usuarios: dict):
    if not usuarios:
        print("  Nenhum usuário cadastrado.")
        return
    for u in usuarios.values():
        print(f"  {u}")