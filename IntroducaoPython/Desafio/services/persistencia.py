import json
import os
from models.Livro import Livro
from models.Usuario import Usuario


ARQUIVO_PADRAO = "biblioteca.json"


def salvar(livros: dict, usuarios: dict, arquivo: str = ARQUIVO_PADRAO):
    dados = {
        "livros":   [l.to_dict() for l in livros.values()],
        "usuarios": [u.to_dict() for u in usuarios.values()],
    }
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"  Dados salvos em '{arquivo}'.")


def carregar(arquivo: str = ARQUIVO_PADRAO) -> tuple[dict, dict]:
    if not os.path.exists(arquivo):
        print("  Nenhum arquivo encontrado. Iniciando com dados vazios.")
        return {}, {}

    with open(arquivo, encoding="utf-8") as f:
        dados = json.load(f)

    livros   = {d["isbn"]:       Livro.from_dict(d)   for d in dados.get("livros",   [])}
    usuarios = {d["id_usuario"]: Usuario.from_dict(d) for d in dados.get("usuarios", [])}

    print(f"  Carregados: {len(livros)} livro(s), {len(usuarios)} usuario(s).")
    return livros, usuarios