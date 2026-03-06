from datetime import datetime, timedelta
from models.Livro import Livro

class Usuario:
    def __init__(self, id_usuario: str, nome: str, cpf: str):
        self._id_usuario = id_usuario
        self._nome = nome
        self._cpf = cpf
        # isbn -> {"titulo": str, "prazo": "YYYY-MM-DD"}
        self._emprestimos: dict = {}

    def __str__(self):
        return (f"[{self._id_usuario}] {self._nome} "
                f"| CPF: {self._cpf} "
                f"| Livros emprestados: {len(self._emprestimos)}")

    def get_id(self):          return self._id_usuario
    def get_nome(self):        return self._nome
    def set_nome(self, nome):  self._nome = nome
    def get_cpf(self):         return self._cpf
    def get_emprestimos(self): return self._emprestimos

    def adicionar_emprestimo(self, livro: Livro, prazo_dias: int = 14):
        prazo = (datetime.now() + timedelta(days=prazo_dias)).strftime("%Y-%m-%d")
        self._emprestimos[livro.get_isbn()] = {
            "titulo": livro.get_titulo(),
            "prazo":  prazo,
        }

    def remover_emprestimo(self, isbn: str):
        if isbn not in self._emprestimos:
            raise ValueError(f"ISBN '{isbn}' não encontrado nos empréstimos deste usuário.")
        del self._emprestimos[isbn]

    def listar_emprestimos(self):
        if not self._emprestimos:
            print("  Nenhum livro emprestado.")
            return
        hoje = datetime.now().date()
        for isbn, info in self._emprestimos.items():
            prazo = datetime.strptime(info["prazo"], "%Y-%m-%d").date()
            alerta = " [ATRASADO]" if prazo < hoje else ""
            print(f"  - '{info['titulo']}' | ISBN: {isbn} | Prazo: {info['prazo']}{alerta}")

    def to_dict(self) -> dict:
        return {
            "id_usuario":  self._id_usuario,
            "nome":        self._nome,
            "cpf":         self._cpf,
            "emprestimos": self._emprestimos,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Usuario":
        u = cls(d["id_usuario"], d["nome"], d["cpf"])
        u._emprestimos = d.get("emprestimos", {})
        return u