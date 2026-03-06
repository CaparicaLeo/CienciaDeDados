class Livro:
    def __init__(self, id_livro: str, titulo: str, autor: str, isbn: str, disponivel: bool = True):
        self._id_livro = id_livro
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._disponivel = disponivel

    def __str__(self):
        status = "[disponivel]" if self._disponivel else "[emprestado]"
        return (f"[{self._id_livro}] '{self._titulo}' — {self._autor} "
                f"| ISBN: {self._isbn} | {status}")

    def get_id(self):          return self._id_livro
    def get_titulo(self):      return self._titulo
    def get_autor(self):       return self._autor
    def get_isbn(self):        return self._isbn
    def get_disponivel(self):  return self._disponivel
    def set_disponivel(self, valor: bool): self._disponivel = valor

    def to_dict(self) -> dict:
        return {
            "id_livro":   self._id_livro,
            "titulo":     self._titulo,
            "autor":      self._autor,
            "isbn":       self._isbn,
            "disponivel": self._disponivel,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Livro":
        return cls(d["id_livro"], d["titulo"], d["autor"], d["isbn"], d["disponivel"])