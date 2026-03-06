from __future__ import annotations
from typing import Optional
from models.Livro import Livro
from models.Usuario import Usuario


def emprestar(livros: dict, usuarios: dict, isbn: str, id_usuario: str, prazo_dias: int = 14):
    livro: Optional[Livro] = livros.get(isbn)
    if not livro:
        raise KeyError(f"Livro com ISBN '{isbn}' não encontrado.")
    if not livro.get_disponivel():
        raise PermissionError(f"'{livro.get_titulo()}' ja esta emprestado.")

    usuario: Optional[Usuario] = usuarios.get(id_usuario)
    if not usuario:
        raise KeyError(f"Usuario '{id_usuario}' não encontrado.")

    livro.set_disponivel(False)
    usuario.adicionar_emprestimo(livro, prazo_dias)


def devolver(livros: dict, usuarios: dict, isbn: str, id_usuario: str):
    livro: Optional[Livro] = livros.get(isbn)
    if not livro:
        raise KeyError(f"Livro com ISBN '{isbn}' não encontrado.")

    usuario: Optional[Usuario] = usuarios.get(id_usuario)
    if not usuario:
        raise KeyError(f"Usuario '{id_usuario}' não encontrado.")

    if isbn not in usuario.get_emprestimos():
        raise ValueError("Este livro não está registrado para este usuário.")

    usuario.remover_emprestimo(isbn)
    livro.set_disponivel(True)