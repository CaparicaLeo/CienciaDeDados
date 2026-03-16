import pandas as pd

df = pd.read_csv(
    'sensores.csv',
    sep = ',',
    usecols= ['sensor_id', 'temperatura', 'pressao', 'status'],
    index_col='sensor_id',
    dtype={
        'temperatura':'float64'
    },
    na_values=['NA', '-']
)
print(df.info())