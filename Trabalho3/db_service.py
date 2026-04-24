import pandas as pd
from sqlalchemy import create_engine

# Use estas configurações para conectar no container
USER = 'dengue_user'
PASSWORD = 'dengue_password'
HOST = 'localhost'  # 'localhost' se o script rodar na sua máquina local
PORT = '3306'
DATABASE = 'dengue_db'

def get_engine():
    """Cria a conexão com o MySQL via SQLAlchemy."""
    url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    return create_engine(url)

def save_to_db(df):
    """Salva o DataFrame no MySQL."""
    engine = get_engine()
    # No MySQL, é importante garantir que o schema exista
    df.to_sql('casos', con=engine, if_exists='replace', index=False)
    print(f"Dados persistidos no MySQL: {DATABASE}.casos")

def get_cases_statistics():
    """Calcula estatísticas de volume diretamente via SQL."""
    engine = get_engine()
    
    # A lógica da subquery permanece idêntica ao SQLite
    query = """
    SELECT 
        AVG(contagem) as media_anual,
        MAX(contagem) as max_anual,
        MIN(contagem) as min_anual
    FROM (
        SELECT nu_ano, COUNT(*) as contagem 
        FROM casos 
        GROUP BY nu_ano
    ) AS estatisticas  -- MySQL exige um alias para subqueries no FROM
    """
    
    with engine.connect() as conn:
        stats = pd.read_sql(query, conn)
    
    return stats.iloc[0]

def get_cases_by_state():
    engine = get_engine()
    query = """
    SELECT sg_uf_not as estado, COUNT(*) as total_casos
    FROM casos
    GROUP BY sg_uf_not
    ORDER BY total_casos DESC
    """
    with engine.connect() as conn:
        df_uf = pd.read_sql(query, conn)
    return df_uf