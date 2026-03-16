import pandas as pd

df = pd.read_csv(
    'transacoes_grandes.csv',
    sep=';',
    index_col='produto',
    dtype={
        'quantidade':'int64',
        'preco_unitario':'float64'
    },
    chunksize=20
)

for i, bloco in enumerate(df):
    print(f"--- Bloco {i + 1} ---")
    print(f"Número de linhas: {len(bloco)}")
    print("3 primeiras linhas do bloco:")
    print(bloco.head(3))
    print("-" * 30)