import matplotlib.pyplot as plt

MAPEAMENTO_UFS = {
    '11': 'Rondônia', '12': 'Acre', '13': 'Amazonas', '14': 'Roraima',
    '15': 'Pará', '16': 'Amapá', '17': 'Tocantins', '21': 'Maranhão',
    '22': 'Piauí', '23': 'Ceará', '24': 'Rio Grande do Norte', '25': 'Paraíba',
    '26': 'Pernambuco', '27': 'Alagoas', '28': 'Sergipe', '29': 'Bahia',
    '31': 'Minas Gerais', '32': 'Espírito Santo', '33': 'Rio de Janeiro',
    '35': 'São Paulo', '41': 'Paraná', '42': 'Santa Catarina', 
    '43': 'Rio Grande do Sul', '50': 'Mato Grosso do Sul', '51': 'Mato Grosso',
    '52': 'Goiás', '53': 'Distrito Federal',
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
    'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
    'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
    'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
}

def generate_charts(df):
    plt.style.use('ggplot')
    
    plt.figure(figsize=(10, 5))
    df['nu_ano'].value_counts().sort_index().plot(kind='bar', color='darkorange')
    plt.title('Evolução Anual de Casos')
    plt.ylabel('Nº de Notificações')
    plt.savefig('casos_por_ano.png')
    
    df['mes'] = df['dt_notific'].dt.month
    plt.figure(figsize=(10, 5))
    df['mes'].value_counts().sort_index().plot(kind='line', marker='o', color='red', linewidth=2)
    plt.title('Sazonalidade: Total de Casos por Mês (Acumulado)')
    plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.grid(True)
    plt.savefig('sazonalidade_mensal.png')
    

def plot_state_ranking(df):
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 8))
    
    df_plot = df.copy()
    
    df_plot['estado_nome'] = df_plot['sg_uf_not'].astype(str).map(MAPEAMENTO_UFS)

    df_plot['estado_nome'] = df_plot['estado_nome'].fillna(df_plot['sg_uf_not'])
    
    state_counts = df_plot['estado_nome'].value_counts().sort_values(ascending=True)
    
    state_counts.plot(kind='barh', color='skyblue', edgecolor='black')
    
    plt.title('Total de Notificações por Estado', fontsize=14, pad=20)
    plt.xlabel('Nº de Casos', fontsize=12)
    plt.ylabel('Estado', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('casos_por_estado_nomes.png')
    print("Gráfico com nomes dos estados gerado com sucesso!")