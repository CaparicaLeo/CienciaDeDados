from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///meu_banco.db')

query = "SELECT * FROM produtos"
df_produtos = pd.read_sql(query, con=engine)

print(df_produtos.head())