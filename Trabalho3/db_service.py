import pandas as pd
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

# ── Configurações de conexão ─────────────────────────────────────────────────
USER     = "dengue_user"
PASSWORD = "dengue_password"
HOST     = "localhost"
PORT     = "3306"
DATABASE = "dengue_db"


def get_engine():
    """Cria e retorna a engine SQLAlchemy para o MySQL."""
    url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    return create_engine(url, pool_pre_ping=True)


def save_to_db(df: pd.DataFrame) -> None:
    """
    Persiste o DataFrame na tabela 'casos' do MySQL.

    Estratégia:
      - Na primeira carga (tabela inexistente) → cria a tabela.
      - Nas cargas seguintes → insere apenas registros novos,
        usando uma tabela temporária + INSERT IGNORE para evitar
        duplicatas sem apagar o histórico existente.

    Usa transação explícita para garantir integridade:
    em caso de erro, o banco volta ao estado anterior.
    """
    engine = get_engine()

    logger.info("Iniciando carga no banco. Registros a processar: %d", len(df))

    try:
        with engine.begin() as conn:  # begin() → commit automático ou rollback em exceção

            # Verifica se a tabela 'casos' já existe
            resultado = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = :db AND table_name = 'casos'"
                ),
                {"db": DATABASE},
            )
            tabela_existe = resultado.scalar() > 0

            if not tabela_existe:
                # Primeira carga: cria a tabela diretamente
                logger.info("Tabela 'casos' não existe. Criando e inserindo dados...")
                df.to_sql("casos", con=conn, if_exists="replace", index=False)
                logger.info("Tabela criada com %d registros.", len(df))
            else:
                # Cargas subsequentes: INSERT IGNORE via tabela temporária
                logger.info("Tabela 'casos' já existe. Inserindo apenas registros novos...")

                df.to_sql("casos_temp", con=conn, if_exists="replace", index=False)

                result = conn.execute(
                    text(
                        "INSERT IGNORE INTO casos "
                        "SELECT * FROM casos_temp"
                    )
                )
                inseridos = result.rowcount

                conn.execute(text("DROP TABLE IF EXISTS casos_temp"))

                logger.info(
                    "%d registros novos inseridos (duplicatas ignoradas).", inseridos
                )

    except Exception as e:
        logger.error("Erro durante a carga no banco: %s", e)
        raise  # Re-lança para que o pipeline registre a falha

    logger.info("Carga finalizada com sucesso em '%s.casos'.", DATABASE)


def get_cases_by_state() -> pd.DataFrame:
    """Retorna o total de casos agrupado por estado, ordenado de forma decrescente."""
    engine = get_engine()
    query = """
        SELECT sg_uf_not AS estado, COUNT(*) AS total_casos
        FROM casos
        GROUP BY sg_uf_not
        ORDER BY total_casos DESC
    """
    logger.info("Consultando ranking de casos por estado...")
    try:
        with engine.connect() as conn:
            df_uf = pd.read_sql(text(query), conn)
        logger.info("Ranking obtido: %d estados.", len(df_uf))
        return df_uf
    except Exception as e:
        logger.error("Erro ao consultar ranking por estado: %s", e)
        raise


def get_cases_statistics() -> pd.Series:
    """
    Calcula estatísticas de volume de casos por ano diretamente via SQL.
    Retorna média, máximo e mínimo de notificações anuais.
    """
    engine = get_engine()
    query = """
        SELECT
            AVG(contagem) AS media_anual,
            MAX(contagem) AS max_anual,
            MIN(contagem) AS min_anual
        FROM (
            SELECT nu_ano, COUNT(*) AS contagem
            FROM casos
            GROUP BY nu_ano
        ) AS estatisticas
    """
    logger.info("Calculando estatísticas anuais via SQL...")
    try:
        with engine.connect() as conn:
            stats = pd.read_sql(text(query), conn)
        logger.info(
            "Estatísticas: média=%.1f | max=%d | min=%d",
            stats.iloc[0]["media_anual"],
            stats.iloc[0]["max_anual"],
            stats.iloc[0]["min_anual"],
        )
        return stats.iloc[0]
    except Exception as e:
        logger.error("Erro ao calcular estatísticas: %s", e)
        raise