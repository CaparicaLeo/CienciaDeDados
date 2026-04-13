import pandas as pd

dados = {
    'Mes': ['Janeiro', 'Fevereiro', 'Março'],
    'Vendas': [15000, 18000, 21000],
    'Meta': ['Sim', 'Sim', 'Sim']
}
relatorio_anual = pd.DataFrame(dados)

relatorio_anual.to_excel('relatorio.xlsx', sheet_name='Resultados', index=False)

try:
    df_dados_brutos = pd.read_excel('arquivo_existente.xlsx', sheet_name='Dados Brutos')
    print("Aba lida com sucesso!")
except FileNotFoundError:
    print("Erro: O arquivo 'arquivo_existente.xlsx' não foi encontrado.")