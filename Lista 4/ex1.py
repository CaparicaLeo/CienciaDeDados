import csv

# csv.reader → acesso por índice
with open("dados.csv") as f:
    leitor = csv.reader(f)
    next(leitor)  # pula o cabeçalho manualmente
    for linha in leitor:
        print(linha[0], linha[1])  # frágil: depende da ordem das colunas

# csv.DictReader → acesso por nome
with open("dados.csv") as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        print(linha["nome"], linha["idade"])  # robusto e legível