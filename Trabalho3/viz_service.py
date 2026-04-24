import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    """Gera gráficos de evolução anual e sazonalidade mensal."""
    plt.style.use('ggplot')
    
    # --- Gráfico 1: Evolução Anual ---
    plt.figure(figsize=(10, 5))
    df['nu_ano'].value_counts().sort_index().plot(kind='bar', color='darkorange')
    plt.title('Evolução Anual de Casos')
    plt.ylabel('Nº de Notificações')
    plt.tight_layout()
    plt.savefig('casos_por_ano.png')
    plt.close()
    
    # --- Gráfico 2: Sazonalidade Mensal ---
    # Garantindo que a coluna de data esteja em datetime
    df['dt_notific'] = pd.to_datetime(df['dt_notific'])
    df['mes'] = df['dt_notific'].dt.month
    
    plt.figure(figsize=(10, 5))
    sazonalidade = df['mes'].value_counts().sort_index()
    
    plt.plot(sazonalidade.index, sazonalidade.values, marker='o', color='red', linewidth=2)
    plt.title('Sazonalidade: Total de Casos por Mês (Acumulado)')
    plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.ylabel('Nº de Casos')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('sazonalidade_mensal.png')
    plt.close()
    print("Gráficos de evolução e sazonalidade gerados com sucesso!")

def plot_state_ranking(df):
    """Gera um gráfico de pizza para a distribuição de casos por estado."""
    plt.style.use('default')
    
    df_plot = df.copy()
    
    # 1. Mapeamento de nomes dos estados
    df_plot['estado_nome'] = df_plot['sg_uf_not'].astype(str).map(MAPEAMENTO_UFS)
    df_plot['estado_nome'] = df_plot['estado_nome'].fillna(df_plot['sg_uf_not'])
    
    # 2. Contagem de casos
    state_counts = df_plot['estado_nome'].value_counts()
    
    # 3. Agrupamento em 'Outros' (Top 10)
    limit = 10
    if len(state_counts) > limit:
        top_states = state_counts.head(limit)
        others_sum = state_counts.iloc[limit:].sum()
        final_counts = pd.concat([top_states, pd.Series({'Outros': others_sum})])
    else:
        final_counts = state_counts

    # 4. Preparação de dados (evita erros de tipo)
    labels_lista = [str(label) for label in final_counts.index.tolist()]
    valores = np.array(final_counts.values)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 5. Geração da Pizza
    pie_output = ax.pie(
        valores, 
        labels=labels_lista,      
        autopct='%1.1f%%',              
        startangle=90,                  
        textprops=dict(color="black"),  
        pctdistance=0.85,               
        explode=[0.05 if i < 3 else 0 for i in range(len(final_counts))] 
    )
    
    wedges = pie_output[0]
    texts = pie_output[1]
    autotexts = pie_output[2] if len(pie_output) > 2 else []
    
    # 6. Estilização
    plt.setp(texts, size=10, weight="bold")    
    plt.setp(autotexts, size=9, color="white", weight="bold") 

    ax.set_title('Distribuição de Notificações por Estado (Top 10)', fontsize=16, pad=20)
    ax.axis('equal')  
    
    ax.legend(
        wedges, 
        labels_lista,
        title="Estados",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    plt.tight_layout()
    plt.savefig('casos_por_estado_pizza.png', bbox_inches='tight')
    plt.close()
    print("Gráfico de pizza gerado com sucesso!")