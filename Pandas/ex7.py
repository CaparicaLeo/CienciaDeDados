import pandas as pd

df = pd.read_csv(
    'experimento.csv',
    sep=',',
    usecols=['amostra', 'ph', 'temperatura', 'concentracao'],
    index_col='amostra',
    dtype={
        'ph':'float32',
        'temperatura':'float32',
        'concentracao':'float32'
    },
)

print(df.head())
print(df.tail())
print(df.describe())