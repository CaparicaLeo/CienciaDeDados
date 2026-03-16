import pandas as pd;

df = pd.read_csv(
    'vendas.csv',
    sep = ';', #Resposta
    encoding = 'utf-8',
    index_col='produto',
    usecols = ['produto', 'quantidade', 'preco_unitario'],
    dtype = {
        'quantidade':'int64',
        'preco_unitario':'float64'
    },
    na_values= ['-','NA']
)
print(df)