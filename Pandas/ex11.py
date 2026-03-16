import pandas as pd

reader = pd.read_csv(
    'dados_sensor_gigante.csv',
    sep=',',
    na_values=['NA', '-'],
    chunksize=10
)

for i, bloco in enumerate(reader):
    media_temp = bloco['temperatura'].mean()
    nulos_temp = bloco['temperatura'].isna().sum()
    
    print(f"--- Bloco {i + 1} ---")
    print(f"Temperatura Média: {media_temp:.2f}")
    print(f"Valores ausentes em 'temperatura': {nulos_temp}")
    print("-" * 30)