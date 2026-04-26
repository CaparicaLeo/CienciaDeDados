import pandas as pd
import logging

logger = logging.getLogger(__name__)


def _decode_age(age_val) -> float | None:
    """
    Decodifica a idade no padrão SINAN:
      - Prefixo 4XXX → anos  (ex: 4025 → 25 anos)
      - Prefixo 3XXX → meses (ex: 3006 → 0.5 anos)
      - Outros prefixos / valores inválidos → None
    Trata NaN de forma explícita antes de qualquer conversão.
    """
    if pd.isna(age_val):
        return None
    try:
        val = str(int(float(age_val)))
        if val.startswith("4"):
            return int(val[1:])
        if val.startswith("3"):
            return int(val[1:]) / 12
        return None
    except (ValueError, TypeError):
        return None


def transform_data(csv_path: str) -> pd.DataFrame:
    """
    Lê o CSV bruto, aplica limpeza e normalizações e retorna
    um DataFrame pronto para ser persistido no banco.

    Etapas:
      1. Filtro por ano (>= 2016)
      2. Parsing de datas (erros viram NaT, linhas removidas ao final)
      3. Decodificação da idade para anos decimais
      4. Criação de colunas auxiliares de mês e ano
      5. Remoção de linhas sem data de notificação
    """
    logger.info("Lendo CSV: %s", csv_path)

    try:
        df = pd.read_csv(csv_path, low_memory=False)
    except FileNotFoundError:
        logger.critical("Arquivo não encontrado: %s", csv_path)
        raise
    except Exception as e:
        logger.critical("Erro ao ler o CSV: %s", e)
        raise

    logger.info("Registros brutos lidos: %d", len(df))

    # --- 1. Filtro por ano ---
    if "nu_ano" not in df.columns:
        logger.error("Coluna 'nu_ano' não encontrada. Colunas disponíveis: %s", df.columns.tolist())
        raise KeyError("Coluna 'nu_ano' ausente no CSV.")

    df = df[df["nu_ano"] >= 2016].copy()
    logger.info("Após filtro de ano (>= 2016): %d registros", len(df))

    # --- 2. Parsing de datas ---
    df["dt_notific"] = pd.to_datetime(df["dt_notific"], errors="coerce")

    datas_invalidas = df["dt_notific"].isna().sum()
    if datas_invalidas > 0:
        logger.warning("%d registros com data inválida serão removidos.", datas_invalidas)

    # --- 3. Decodificação da idade ---
    df["idade_anos"] = df["nu_idade_n"].apply(_decode_age)

    # --- 4. Colunas auxiliares ---
    df["mes_notific"] = df["dt_notific"].dt.month
    df["ano_notific"] = df["dt_notific"].dt.year

    # --- 5. Remoção de linhas sem data ---
    df = df.dropna(subset=["dt_notific"])

    logger.info("Transformação concluída. %d registros processados.", len(df))
    return df