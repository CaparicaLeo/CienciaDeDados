import pandas as pd
import logging

logger = logging.getLogger(__name__)


def run_transform():
    logger.info("Iniciando transformacao dos dados...")

    df = pd.read_csv("dados_dengue.csv", low_memory=False)

    logger.info("Colunas disponiveis (%d): %s", len(df.columns), list(df.columns))
    logger.info("Shape original: %s", df.shape)
    logger.info("Amostra dos dados:\n%s", df.head(3).to_string())

    duplicadas = df.duplicated().sum()
    if duplicadas > 0:
        df = df.drop_duplicates()
        logger.info("Removidas %d linhas duplicadas.", duplicadas)

    nulos_por_coluna = df.isnull().sum()
    nulos_total = nulos_por_coluna.sum()
    if nulos_total > 0:
        colunas_com_nulo = nulos_por_coluna[nulos_por_coluna > 0]
        logger.info("Colunas com nulos:\n%s", colunas_com_nulo.to_string())
        colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns
        for col in colunas_numericas:
            if df[col].isnull().sum() > 0:
                n_nulos = df[col].isnull().sum()
                mediana = df[col].median()
                if pd.isna(mediana):
                    mediana = 0
                    logger.info("Coluna '%s': mediana nula, fallback 0 para %d nulos.", col, n_nulos)
                else:
                    logger.info("Coluna '%s': %d nulos preenchidos com mediana=%.4f.", col, n_nulos, mediana)
                df[col] = df[col].fillna(mediana)
        colunas_texto = df.select_dtypes(include=["object"]).columns
        for col in colunas_texto:
            if df[col].isnull().sum() > 0:
                n_nulos = df[col].isnull().sum()
                df[col] = df[col].fillna("")
                logger.info("Coluna '%s': %d nulos preenchidos com string vazia.", col, n_nulos)

    colunas_data = [c for c in df.columns if c.startswith("dt_")]
    for col in colunas_data:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Desfragmentar antes de adicionar colunas
    df = df.copy()

    colunas_categoricas = [
        "sg_uf_not", "sg_uf", "cs_sexo", "cs_raca", "cs_gestant", "cs_escol_n",
        "classi_fin", "criterio", "evolucao", "tpautocto", "id_agravo",
    ]
    for col in colunas_categoricas:
        if col in df.columns:
            df[col] = df[col].astype(str)

    # Targets binarios (pd.to_numeric trata "2.0" como float, 2.0 == 2)
    # Nota: 'obito' eh o target preferencial, mas se tiver < 5 casos positivos,
    # o model_service fara fallback automatico para 'hospitaliz_bin' via _selecionar_target().
    # O relatorio final reflete o target real utilizado por cada modelo.
    if "evolucao" in df.columns:
        df["obito"] = (pd.to_numeric(df["evolucao"], errors="coerce") == 2).astype(int)
        logger.info("Target 'obito' criado. Obitos: %d / Total: %d",
                     df["obito"].sum(), len(df))

    if "hospitaliz" in df.columns:
        df["hospitaliz_bin"] = (pd.to_numeric(df["hospitaliz"], errors="coerce") == 1).astype(int)
        logger.info("Target 'hospitaliz_bin' criado. Hospitalizados: %d / Total: %d",
                     df["hospitaliz_bin"].sum(), len(df))

    if "nu_idade_n" in df.columns:
        df["nu_idade_n"] = pd.to_numeric(df["nu_idade_n"], errors="coerce").fillna(0).astype(int)
        df["idade_anos"] = df["nu_idade_n"] // 12
        df.loc[df["idade_anos"] > 120, "idade_anos"] = 0
        logger.info("Faixa etaria: %d a %d anos",
                     df["idade_anos"].min(), df["idade_anos"].max())

    if "nu_ano" in df.columns and "sg_uf_not" in df.columns:
        agg_casos = df.groupby(["nu_ano", "sg_uf_not"]).agg(
            total_casos=("nu_ano", "count"),
            total_obitos=pd.NamedAgg(column="obito", aggfunc="sum") if "obito" in df.columns else None,
        ).reset_index()
        if "obito" in df.columns:
            agg_casos["taxa_mortalidade"] = (
                agg_casos["total_obitos"] / agg_casos["total_casos"] * 100
            )
        logger.info("Agregacao por ano/UF criada com %d linhas.", len(agg_casos))

    df_agg_semana = None
    if "sem_not" in df.columns:
        df["sem_not"] = df["sem_not"].astype(str)
        df_agg_semana = df.groupby("sem_not").agg(
            casos=("sem_not", "count"),
            nu_ano=("nu_ano", "first"),
            sg_uf_not=("sg_uf_not", "first"),
        ).reset_index()
        df_agg_semana["sem_not_num"] = range(1, len(df_agg_semana) + 1)
        logger.info("Agregacao por semana (sem_not) criada com %d linhas.", len(df_agg_semana))

    df.to_csv("dados_limpos.csv", index=False)
    logger.info("Arquivo 'dados_limpos.csv' salvo (%d linhas).", len(df))

    return df, df_agg_semana
