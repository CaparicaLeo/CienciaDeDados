import pandas as pd

df_vendas = pd.read_csv(
    'vendas.csv', 
    header=None,       
    index_col=0,      
    na_values="ND"     
)

print(df_vendas.head())