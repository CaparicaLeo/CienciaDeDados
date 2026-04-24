import api_service 
from transform_service import transform_data
from db_service import save_to_db, get_cases_by_state
# Adicionei o generate_charts no import
from viz_service import plot_state_ranking, generate_charts

def run_pipeline():
    print("🚀 Iniciando Pipeline de Dados (Versão MySQL + Docker)...")
    
    # Passo 1: Coleta (API do Governo)
    print("📡 Passo 1: Coletando dados da API do Datasus...")
    api_service.run_extraction()
    
    # Passo 2: Tratamento (Limpeza e Conversão)
    print("🧹 Passo 2: Tratando e normalizando os dados...")
    df_clean = transform_data('dados_dengue.csv')
    
    # Passo 3: Banco de Dados (Agora no MySQL via Docker)
    # Certifique-se que o container MySQL esteja rodando (docker-compose up -d)
    print("🗄️ Passo 3: Armazenando no banco MySQL...")
    save_to_db(df_clean)
    
    # Passo 4: Análise Exploratória (Ranking de Estados)
    print("\n" + "="*40)
    print("📊 ANÁLISE: RANKING DE ESTADOS (Recuperado do Banco)")
    # Aqui buscamos os dados que acabamos de salvar no MySQL
    df_uf = get_cases_by_state()
    print(df_uf.head(10).to_string(index=False)) 
    print("="*40)
    
    # Passo 5: Visualização (Gráficos)
    print("\n📈 Passo 4: Gerando gráficos e visualizações...")
    
    # Gráfico de Barras/Linha (Evolução Temporal)
    generate_charts(df_clean)
    
    # Gráfico de Pizza (Distribuição por Estado)
    # Usamos o df_clean tratado para ter os dados completos
    plot_state_ranking(df_clean)
    
    print("\n✅ Pipeline finalizado com sucesso!")
    print("📂 Verifique o Banco MySQL e as imagens: "
          "\n   - casos_por_ano.png"
          "\n   - sazonalidade_mensal.png"
          "\n   - casos_por_state_pizza.png")

if __name__ == "__main__":
    run_pipeline()