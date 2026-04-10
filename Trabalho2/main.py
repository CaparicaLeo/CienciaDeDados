import api_service 
from transform_service import transform_data
from db_service import save_to_db, get_cases_by_state
from viz_service import generate_charts

def run_pipeline():
    print("🚀 Iniciando Pipeline de Dados Completo...")
    
    # Passo 1: Coleta (API do Governo)
    # Aqui ele executa o script que busca 2000 registros por ano
    print("📡 Passo 1: Coletando dados da API do Datasus...")
    api_service.run_extraction()
    
    # Passo 2: Tratamento (Limpeza e Conversão)
    print("🔄 Passo 2: Tratando e normalizando os dados...")
    df_clean = transform_data('dados_dengue.csv')
    
    # Passo 3: Banco de Dados (Persistência Relacional)
    print("🗄️ Passo 3: Armazenando no banco SQLite...")
    save_to_db(df_clean)
    
    # Passo 4: Análise Exploratória (Ranking de Estados)
    # Isso atende ao requisito de "Calcular estatísticas"
    print("\n" + "="*40)
    print("📊 ANÁLISE: RANKING DE ESTADOS (Na amostra)")
    df_uf = get_cases_by_state()
    print(df_uf.head(10).to_string(index=False)) 
    print("="*40)
    
    # Passo 5: Visualização (Gráficos)
    print("\n📈 Passo 4: Gerando gráficos e visualizações...")
    generate_charts(df_clean)
    
    print("\n✅ Pipeline finalizado com sucesso!")
    print("📂 Verifique os arquivos: dengue_data.db e as imagens .png")

if __name__ == "__main__":
    run_pipeline()