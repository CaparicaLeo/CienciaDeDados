import pandas as pd

df = pd.read_csv(
    'log_sistema.csv',
    sep=',',
    encoding='utf-8',
    parse_dates=['timestamp'],
    index_col='id_evento',
    usecols=['id_evento','tipo','timestamp', 'descricao'],
    engine='python',
    skiprows=2,
    nrows=2
)

print(df)