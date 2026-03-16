import pandas as pd

df = pd.read_csv(
    'big_data_simulado.csv',
    sep=',',
    usecols=['id', 'coluna_a', 'coluna_b', 'coluna_c', 'timestamp'],
    index_col='id',
    dtype={
        'coluna_b':'float16',
    }
)

print(df.info())