class Biblioteca:
    def __init__(self, livros=[]):
        self.livros = livros
    
    def adicionar_livro(self, livro):
        self.livros.append(livro)
    def remover_livro(self, livro):
        self.livros.remove(livro)
    def listar_livros(self):
        return self.livros
    def emprestar_livro(self, livro, usuario):
        if livro in self.livros:
            self.remover_livro(livro)
            usuario.adicionar_livro(livro)
    def devolver_livro(self, livro, usuario):
        if livro in usuario.get_livros():
            usuario.remover_livro(livro)
            self.adicionar_livro(livro)
    

    