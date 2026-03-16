import pandas as pd

df = pd.read_csv(
    'notas.csv',
    sep=',',
    index_col='aluno'
)

print(df.describe())