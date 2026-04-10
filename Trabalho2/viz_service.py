import matplotlib.pyplot as plt
import seaborn as sns

def generate_charts(df):
    plt.style.use('ggplot')
    
    # Gráfico 1: Casos por Ano (Barra)
    plt.figure(figsize=(10, 5))
    df['nu_ano'].value_counts().sort_index().plot(kind='bar', color='darkorange')
    plt.title('Evolução Anual de Casos')
    plt.ylabel('Nº de Notificações')
    plt.savefig('casos_por_ano.png')
    
    # Gráfico 2 (Interesse): Sazonalidade Mensal
    # Extraímos o mês da data de notificação
    df['mes'] = df['dt_notific'].dt.month
    plt.figure(figsize=(10, 5))
    df['mes'].value_counts().sort_index().plot(kind='line', marker='o', color='red', linewidth=2)
    plt.title('Sazonalidade: Total de Casos por Mês (Acumulado)')
    plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.grid(True)
    plt.savefig('sazonalidade_mensal.png')
    

def plot_monthly_distribution(df):
    # Extrai o mês da data de notificação
    df['mes'] = df['dt_notific'].dt.month
    plt.figure(figsize=(10, 6))
    df['mes'].value_counts().sort_index().plot(kind='line', marker='o')
    plt.title('Distribuição Mensal (Amostra de 2000/ano)')
    plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.savefig('sazonalidade_amostra.png')