class Veiculo:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def exibir_informacoes(self):
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Ano: {self.ano}")
    
    def tipo_habilitacao(self):
        return "Tipo de habilitação não especificado"
    
class Carro(Veiculo):
    def __init__(self, marca, modelo, ano, numero_portas):
        super().__init__(marca, modelo, ano)
        self.numero_portas = numero_portas

    def exibir_informacoes(self):
        super().exibir_informacoes()
        print(f"Número de portas: {self.numero_portas}")
    
    def tipo_habilitacao(self):
        return "Habilitação categoria B"

class Moto(Veiculo):
    def __init__(self, marca, modelo, ano, cilindradas):
        super().__init__(marca, modelo, ano)
        self.cilindradas = cilindradas

    def exibir_informacoes(self):
        super().exibir_informacoes()
        print(f"Cilindradas: {self.cilindradas} cc")
    
    def tipo_habilitacao(self):
        return "Habilitação categoria A"
    
if __name__ == "__main__":
    print("1. Exibir informações do carro")
    print("2. Exibir informações da moto")
    print("3. Informações gerais")
    print("4. Sair")