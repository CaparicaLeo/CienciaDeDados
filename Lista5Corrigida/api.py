import requests
import pandas as pd

url = "https://api.dados.exemplo/usuarios"

try:
    response = requests.get(url)
    response.raise_for_status() 

    dados_json = response.json()
    df_usuarios = pd.DataFrame(dados_json)
    
    print(df_usuarios.info())
except Exception as e:
    print(f"Erro na requisição: {e}")