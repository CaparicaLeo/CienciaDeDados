import pandas as pd

df = pd.read_csv(
    'transacoes.csv',
    sep=',',
    encoding='utf-8',
    usecols=['id_transacao', 'valor', 'moeda'],
    index_col='id_transacao',
    dtype={
        'valor':'str'
    },
)
df['valor'] = df['valor'].str.replace('.', '', n=1, regex=False)
df['valor'] = df['valor'].astype(float)

print(df)