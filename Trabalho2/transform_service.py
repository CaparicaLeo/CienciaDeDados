import pandas as pd

def transform_data(csv_path):
    # 'low_memory=False' resolve o DtypeWarning das colunas mistas
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Criamos uma cópia para evitar o PerformanceWarning de fragmentação
    df = df[df['nu_ano'] >= 2016].copy()
    
    # 1. Tratamento de Datas
    df['dt_notific'] = pd.to_datetime(df['dt_notific'], errors='coerce')
    
    # 2. Tratamento da Idade (Mantemos para filtros, mas focaremos no volume)
    def decode_age(age_str):
        try:
            val = str(int(float(age_str)))
            if val.startswith('4'): return int(val[1:]) 
            if val.startswith('3'): return int(val[1:]) / 12 
            return None
        except: return None

    df['idade_anos'] = df['nu_idade_n'].apply(decode_age)
    
    # 3. Criar coluna de Mês e Ano para facilitar agrupamentos de volume
    df['mes_notific'] = df['dt_notific'].dt.month
    
    # Removemos linhas sem data, pois são inúteis para contar casos por período
    df = df.dropna(subset=['dt_notific'])
    
    print(f"✅ Transformação concluída. {len(df)} registros processados.")
    return df