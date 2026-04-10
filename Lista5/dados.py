import csv

precos = []
with open('produtos.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['categoria'] == 'Eletrônicos':
            precos.append(float(r['preco']))

print(f"Média: {sum(precos)/len(precos) if precos else 0}")