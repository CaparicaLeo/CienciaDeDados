import logging
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import learning_curve

logger = logging.getLogger(__name__)

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 12


def _salvar(fig, nome):
    path = f"{nome}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    logger.info("Grafico salvo: %s", path)
    plt.close(fig)


def plot_metricas_comparativas(resultados):
    logger.info("Gerando grafico comparativo de metricas...")

    dados = []
    for r in resultados:
        if r["tipo"] == "classificacao":
            dados.append({"Modelo": r["modelo"], "Acuracia": r["accuracy"],
                          "Precisao": r["precision"], "Recall": r["recall"],
                          "F1-Score": r["f1"]})
        elif r["tipo"] == "regressao":
            dados.append({"Modelo": r["modelo"], "R²": r["r2"]})

    if not dados:
        logger.warning("Sem dados para grafico comparativo.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Grafico de classificacao
    class_data = [d for d in dados if "Acuracia" in d]
    if class_data:
        df_class = pd.DataFrame(class_data)
        df_melt = df_class.melt(id_vars="Modelo", var_name="Metrica", value_name="Valor")
        sns.barplot(data=df_melt, x="Modelo", y="Valor", hue="Metrica", ax=axes[0])
        axes[0].set_title("Metricas - Classificacao", fontsize=14)
        axes[0].set_ylabel("Valor")
        axes[0].set_ylim(0, 1.05)
        axes[0].legend(loc="lower right")
    else:
        axes[0].text(0.5, 0.5, "Sem dados de classificacao", ha="center", va="center")
        axes[0].set_title("Classificacao", fontsize=14)

    # Grafico de regressao
    reg_data = [d for d in dados if "R²" in d]
    if reg_data:
        df_reg = pd.DataFrame(reg_data)
        df_melt_r = df_reg.melt(id_vars="Modelo", var_name="Metrica", value_name="Valor")
        sns.barplot(data=df_melt_r, x="Modelo", y="Valor", hue="Metrica", ax=axes[1])
        axes[1].set_title("Metricas - Regressao", fontsize=14)
        axes[1].set_ylabel("Valor")
        axes[1].legend(loc="lower right")
    else:
        axes[1].text(0.5, 0.5, "Sem dados de regressao", ha="center", va="center")
        axes[1].set_title("Regressao", fontsize=14)

    fig.tight_layout()
    _salvar(fig, "grafico_metricas_comparativas")


def plot_confusion_matrix(resultados):
    logger.info("Gerando matrizes de confusao...")

    class_results = [r for r in resultados if r["tipo"] == "classificacao" and "confusion_matrix" in r]

    if not class_results:
        logger.warning("Nenhum resultado de classificacao para matriz de confusao.")
        return

    n = len(class_results)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))
    if n == 1:
        axes = [axes]

    for ax, r in zip(axes, class_results):
        cm = r["confusion_matrix"]
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                    xticklabels=["Sobreviveu", "Obito"],
                    yticklabels=["Sobreviveu", "Obito"])
        ax.set_title(f"Matriz de Confusao - {r['modelo']}", fontsize=13)
        ax.set_xlabel("Predito")
        ax.set_ylabel("Real")

    fig.tight_layout()
    _salvar(fig, "grafico_confusion_matrix")


def plot_regressoes(resultados):
    logger.info("Gerando graficos de dispersao real vs previsto...")

    reg_results = [r for r in resultados if r["tipo"] == "regressao"]

    if not reg_results:
        logger.warning("Nenhum resultado de regressao para scatter plot.")
        return

    n = len(reg_results)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))
    if n == 1:
        axes = [axes]

    for ax, r in zip(axes, reg_results):
        y_test = r["y_test"]
        y_pred = r["y_pred"]
        ax.scatter(y_test, y_pred, alpha=0.6, edgecolors="k", linewidth=0.5)
        limite = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
        ax.plot(limite, limite, "r--", linewidth=1.5, label="Ideal")
        ax.set_xlabel("Valor Real")
        ax.set_ylabel("Valor Previsto")
        ax.set_title(f"{r['modelo']}\nR² = {r.get('r2', 0):.4f} | RMSE = {r.get('rmse', 0):.2f}",
                     fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    _salvar(fig, "grafico_regressoes")


def plot_curva_aprendizado(df, resultados):
    logger.info("Gerando curva de aprendizado (KNN)...")

    target_cols = [c for c in ["obito", "hospitaliz_bin"] if c in df.columns]
    target = None
    for c in target_cols:
        if df[c].nunique() >= 2:
            target = c
            break

    if target is None:
        logger.warning("Nenhum target binario viavel para curva de aprendizado. Pulando.")
        return

    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import learning_curve

    feature_cols = [c for c in ["idade_anos", "febre", "mialgia", "cefaleia", "exantema",
                                "vomito", "nausea", "dor_costas", "dor_retro"]
                    if c in df.columns]
    if len(feature_cols) < 3:
        logger.warning("Poucas features para curva de aprendizado. Pulando.")
        return

    X = df[feature_cols].copy()
    for c in X.columns:
        X[c] = pd.to_numeric(X[c], errors="coerce").fillna(0)
    y = df[target]

    model = KNeighborsClassifier(n_neighbors=5)

    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring="accuracy", random_state=42
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                    alpha=0.2, color="blue")
    ax.fill_between(train_sizes, test_mean - test_std, test_mean + test_std,
                    alpha=0.2, color="orange")
    ax.plot(train_sizes, train_mean, "o-", color="blue", label="Treino")
    ax.plot(train_sizes, test_mean, "o-", color="orange", label="Validacao")
    ax.set_xlabel("Exemplos de Treino")
    ax.set_ylabel("Acuracia")
    ax.set_title("Curva de Aprendizado - KNN", fontsize=14)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

    _salvar(fig, "grafico_curva_aprendizado")


def plot_distribuicao_casos(df):
    logger.info("Gerando grafico de distribuicao de casos por ano...")

    if "nu_ano" not in df.columns:
        logger.warning("Coluna 'nu_ano' nao encontrada. Pulando distribuicao.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    contagem_ano = df["nu_ano"].value_counts().sort_index()
    axes[0].bar(contagem_ano.index.astype(str), contagem_ano.values, color="steelblue")
    axes[0].set_title("Casos por Ano", fontsize=14)
    axes[0].set_xlabel("Ano")
    axes[0].set_ylabel("Numero de Casos")
    axes[0].tick_params(axis="x", rotation=45)

    if "obito" in df.columns:
        obitos_ano = df.groupby("nu_ano")["obito"].sum()
        axes[1].bar(obitos_ano.index.astype(str), obitos_ano.values, color="indianred")
        axes[1].set_title("Obitos por Ano", fontsize=14)
        axes[1].set_xlabel("Ano")
        axes[1].set_ylabel("Numero de Obitos")
        axes[1].tick_params(axis="x", rotation=45)
    else:
        axes[1].text(0.5, 0.5, "Dados de obito indisponiveis",
                     ha="center", va="center")

    fig.tight_layout()
    _salvar(fig, "grafico_distribuicao_casos")


def plot_mapa_brasil(df):
    logger.info("Gerando mapa do Brasil com distribuicao de casos...")

    if "sg_uf_not" not in df.columns:
        logger.warning("Coluna 'sg_uf_not' nao encontrada. Pulando mapa.")
        return

    try:
        import geopandas as gpd
    except ImportError:
        logger.warning("geopandas nao instalado. Pulando mapa.")
        return

    casos_por_uf = df["sg_uf_not"].value_counts().reset_index()
    casos_por_uf.columns = ["codigo_ibg", "casos"]
    casos_por_uf["codigo_ibg"] = casos_por_uf["codigo_ibg"].astype(str)

    url = (
        "https://raw.githubusercontent.com/codeforamerica/"
        "click_that_hood/master/public/data/brazil-states.geojson"
    )
    try:
        gdf = gpd.read_file(url)
    except Exception as e:
        logger.warning("Erro ao carregar GeoJSON do Brasil: %s", e)
        return

    gdf = gdf.merge(casos_por_uf, on="codigo_ibg", how="left")
    gdf["casos"] = gdf["casos"].fillna(0).astype(int)

    fig, ax = plt.subplots(figsize=(12, 10))
    gdf.plot(
        column="casos",
        cmap="YlOrRd",
        edgecolor="black",
        linewidth=0.5,
        legend=True,
        ax=ax,
        legend_kwds={"label": "Casos", "shrink": 0.6},
    )

    for _, row in gdf.iterrows():
        if row["casos"] > 0:
            ax.annotate(
                row["sigla"],
                xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                ha="center", va="center",
                fontsize=8, color="black", fontweight="bold",
            )

    ax.set_title("Distribuicao de Casos de Dengue por Estado", fontsize=15)
    ax.axis("off")
    _salvar(fig, "grafico_mapa_brasil")


def plot_roc_curve_logistica(resultados):
    logger.info("Gerando curva ROC para Regressao Logistica...")

    log_result = next(
        (r for r in resultados if r.get("modelo") == "Regressao Logistica" and "y_prob" in r),
        None
    )
    if log_result is None:
        logger.warning("Resultado da Regressao Logistica nao encontrado para curva ROC.")
        return

    from sklearn.metrics import roc_curve

    y_test = log_result["y_test"]
    y_prob = log_result["y_prob"]
    auc = log_result.get("roc_auc", 0)

    fpr, tpr, _ = roc_curve(y_test, y_prob)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, "b-", linewidth=2, label=f"ROC Curve (AUC = {auc:.4f})")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Aleatorio")
    ax.set_xlabel("Taxa de Falsos Positivos (FPR)")
    ax.set_ylabel("Taxa de Verdadeiros Positivos (TPR)")
    ax.set_title("Curva ROC - Regressao Logistica", fontsize=14)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    _salvar(fig, "grafico_roc_logistica")


def plot_coeficientes_logistica(resultados):
    logger.info("Gerando grafico de coeficientes da Regressao Logistica...")

    log_result = next(
        (r for r in resultados if r.get("modelo") == "Regressao Logistica" and "coef" in r),
        None
    )
    if log_result is None:
        logger.warning("Coeficientes da Regressao Logistica nao encontrados.")
        return

    coef = np.array(log_result["coef"])
    features = log_result["feature_names"]

    idx = np.argsort(np.abs(coef))

    fig, ax = plt.subplots(figsize=(10, max(6, len(features) * 0.35)))
    colors = ["coral" if c < 0 else "steelblue" for c in coef[idx]]
    ax.barh(range(len(features)), coef[idx], color=colors)
    ax.set_yticks(range(len(features)))
    ax.set_yticklabels([features[i] for i in idx])
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Coeficiente")
    ax.set_title("Coeficientes da Regressao Logistica", fontsize=14)
    ax.grid(True, alpha=0.3, axis="x")

    _salvar(fig, "grafico_coeficientes_logistica")


def plot_alpha_curve(resultados):
    logger.info("Gerando curva de tuning de alpha (Ridge + Lasso)...")

    reg_results = [r for r in resultados if r.get("alpha_curve") is not None]
    if not reg_results:
        logger.warning("Nenhum resultado com curva de alpha encontrado.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    for r in reg_results:
        ac = r["alpha_curve"]
        ax.semilogx(ac["alphas"], ac["scores"], "o-",
                     label=f"{r['modelo']} (melhor alpha={ac['best_alpha']:.4f})")

    ax.set_xlabel("Alpha (escala log)")
    ax.set_ylabel("R²")
    ax.set_title("Tuning de Regularizacao - Ridge vs Lasso", fontsize=14)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

    _salvar(fig, "grafico_alpha_curve")


def run_viz(df, resultados):
    logger.info("=" * 60)
    logger.info("INICIANDO GERACAO DE GRAFICOS")
    logger.info("=" * 60)

    sns.set_theme(style="whitegrid")

    plot_metricas_comparativas(resultados)
    plot_confusion_matrix(resultados)
    plot_regressoes(resultados)
    plot_curva_aprendizado(df, resultados)
    plot_distribuicao_casos(df)
    plot_mapa_brasil(df)
    plot_roc_curve_logistica(resultados)
    plot_coeficientes_logistica(resultados)
    plot_alpha_curve(resultados)

    logger.info("=" * 60)
    logger.info("GERACAO DE GRAFICOS FINALIZADA")
    logger.info("=" * 60)
