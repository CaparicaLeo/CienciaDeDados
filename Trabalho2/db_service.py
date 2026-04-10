import sqlite3
import pandas as pd

def save_to_db(df, db_name="dengue_data.db"):
    """Salva o DataFrame no banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    # Salva os dados na tabela 'casos'
    df.to_sql('casos', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Dados persistidos no banco {db_name}")

def get_cases_statistics(db_name="dengue_data.db"):
    """Calcula estatísticas de volume diretamente via SQL."""
    conn = sqlite3.connect(db_name)
    
    query = """
    SELECT 
        AVG(contagem) as media_anual,
        MAX(contagem) as max_anual,
        MIN(contagem) as min_anual
    FROM (
        SELECT nu_ano, COUNT(*) as contagem 
        FROM casos 
        GROUP BY nu_ano
    )
    """
    
    stats = pd.read_sql(query, conn)
    conn.close()
    
    # Retorna uma série com os índices: media_anual, max_anual, min_anual
    return stats.iloc[0]

def get_cases_by_state(db_name="dengue_data.db"):
    conn = sqlite3.connect(db_name)
    query = """
    SELECT sg_uf_not as estado, COUNT(*) as total_casos
    FROM casos
    GROUP BY sg_uf_not
    ORDER BY total_casos DESC
    """
    df_uf = pd.read_sql(query, conn)
    conn.close()
    return df_uf