import pandas as pd

df = pd.read_csv(
    'estoque.csv',
    sep=';',
    encoding='utf-8',
    usecols=['item', 'valor_unitario', 'peso_kg'],
    index_col='item',
    dtype = {
        'valor_unitario':'float32',
        'peso':'float32'
    },
    decimal=','
)

print(df.dtypes)