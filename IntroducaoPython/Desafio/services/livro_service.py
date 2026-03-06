from models.Livro import Livro


def adicionar(livros: dict, livro: Livro):
    if livro.get_isbn() in livros:
        raise ValueError(f"ISBN '{livro.get_isbn()}' já cadastrado.")
    livros[livro.get_isbn()] = livro


def remover(livros: dict, isbn: str):
    if isbn not in livros:
        raise KeyError(f"Livro com ISBN '{isbn}' não encontrado.")
    del livros[isbn]


def buscar_por_titulo(livros: dict, trecho: str) -> list[Livro]:
    t = trecho.lower()
    return [l for l in livros.values() if t in l.get_titulo().lower()]


def buscar_por_autor(livros: dict, trecho: str) -> list[Livro]:
    t = trecho.lower()
    return [l for l in livros.values() if t in l.get_autor().lower()]


def buscar_por_isbn(livros: dict, isbn: str) -> Livro | None:
    return livros.get(isbn)


def listar(livros: dict):
    if not livros:
        print("  Nenhum livro cadastrado.")
        return
    for l in livros.values():
        print(f"  {l}")