import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

MAPEAMENTO_UFS = {
    "11": "Rondônia",   "12": "Acre",      "13": "Amazonas",         "14": "Roraima",
    "15": "Pará",       "16": "Amapá",     "17": "Tocantins",        "21": "Maranhão",
    "22": "Piauí",      "23": "Ceará",     "24": "Rio Grande do Norte", "25": "Paraíba",
    "26": "Pernambuco", "27": "Alagoas",   "28": "Sergipe",          "29": "Bahia",
    "31": "Minas Gerais","32": "Espírito Santo","33": "Rio de Janeiro","35": "São Paulo",
    "41": "Paraná",     "42": "Santa Catarina","43": "Rio Grande do Sul","50": "Mato Grosso do Sul",
    "51": "Mato Grosso","52": "Goiás",     "53": "Distrito Federal",
    "AC": "Acre",  "AL": "Alagoas",  "AP": "Amapá",  "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará",    "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais","PA": "Pará","PB": "Paraíba","PR": "Paraná",
    "PE": "Pernambuco","PI": "Piauí","RJ": "Rio de Janeiro","RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul","RO": "Rondônia","RR": "Roraima","SC": "Santa Catarina",
    "SP": "São Paulo","SE": "Sergipe","TO": "Tocantins",
}

MESES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
            "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def generate_charts(df: pd.DataFrame) -> None:
    """
    Gera dois gráficos de análise temporal:
      1. Gráfico de barras — evolução anual de notificações
      2. Gráfico de linha  — sazonalidade mensal acumulada

    Análise esperada dos resultados:
      - O gráfico anual revela tendências epidemiológicas: anos de surto
        (ex.: 2019 e 2022 registraram picos históricos no Brasil) versus
        anos de queda, mostrando o comportamento cíclico da dengue.
      - O gráfico de sazonalidade expõe a concentração de casos nos meses
        de verão (jan–abr), período de chuvas intensas que favorecem a
        reprodução do Aedes aegypti. O vale ocorre tipicamente entre
        jun–set (inverno/seca).
    """
    plt.style.use("ggplot")

    # ── Gráfico 1: Evolução Anual (Barras) ───────────────────────────────────
    logger.info("Gerando gráfico de evolução anual...")

    contagem_anual = df["nu_ano"].value_counts().sort_index()
    stats = contagem_anual.describe()

    fig, ax = plt.subplots(figsize=(11, 5))

    bars = ax.bar(
        contagem_anual.index.astype(str),
        contagem_anual.values,
        color="darkorange",
        edgecolor="white",
        linewidth=0.5,
    )

    # Destaque visual no ano de maior pico
    idx_max = contagem_anual.values.argmax()
    bars[idx_max].set_color("crimson")
    bars[idx_max].set_label(f"Pico: {contagem_anual.index[idx_max]}")

    # Linha de média
    ax.axhline(stats["mean"], color="navy", linestyle="--", linewidth=1.2,
               label=f"Média: {stats['mean']:,.0f}")

    ax.set_title("Evolução Anual de Notificações de Dengue (2016–2025)",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Nº de Notificações", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(fontsize=9)

    # Caixa de estatísticas descritivas (calculadas com pandas)
    texto_stats = (
        f"Estatísticas (pandas)\n"
        f"Total:  {contagem_anual.sum():,}\n"
        f"Média:  {stats['mean']:,.0f}\n"
        f"Mediana:{contagem_anual.median():,.0f}\n"
        f"Desvio: {stats['std']:,.0f}\n"
        f"Mín:    {int(stats['min']):,}\n"
        f"Máx:    {int(stats['max']):,}"
    )
    ax.text(
        0.98, 0.97, texto_stats,
        transform=ax.transAxes, fontsize=8,
        verticalalignment="top", horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("casos_por_ano.png", dpi=150)
    plt.close()
    logger.info("casos_por_ano.png salvo.")

    # ── Gráfico 2: Histograma de Idades ─────────────────────────────────────
    logger.info("Gerando histograma de distribuição de idades...")

    idades = df["idade_anos"].dropna()
    idades = idades[(idades >= 0) & (idades <= 100)]  # remove outliers extremos

    fig, ax = plt.subplots(figsize=(11, 5))

    n, bins, patches = ax.hist(
        idades,
        bins=30,
        color="steelblue",
        edgecolor="white",
        linewidth=0.5,
    )

    # Colorir a faixa de maior incidência (moda visual)
    idx_max = n.argmax()
    patches[idx_max].set_facecolor("crimson")
    patches[idx_max].set_label(
        f"Faixa mais afetada: {bins[idx_max]:.0f}–{bins[idx_max+1]:.0f} anos"
    )

    # Linhas de média e mediana
    media  = idades.mean()
    mediana = idades.median()
    ax.axvline(media,   color="darkorange", linestyle="--", linewidth=1.5, label=f"Média: {media:.1f} anos")
    ax.axvline(mediana, color="green",      linestyle=":",  linewidth=1.5, label=f"Mediana: {mediana:.1f} anos")

    ax.set_title("Distribuição de Casos de Dengue por Faixa Etária",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Idade (anos)", fontsize=11)
    ax.set_ylabel("Nº de Casos", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")

    # Estatísticas descritivas com pandas
    stats_idade = idades.describe()
    texto_stats_i = (
        f"Estatísticas (pandas)\n"
        f"Total:  {int(stats_idade['count']):,}\n"
        f"Média:  {stats_idade['mean']:.1f} anos\n"
        f"Mediana:{mediana:.1f} anos\n"
        f"Desvio: {stats_idade['std']:.1f}\n"
        f"Mín:    {stats_idade['min']:.0f} anos\n"
        f"Máx:    {stats_idade['max']:.0f} anos"
    )
    ax.text(
        0.98, 0.97, texto_stats_i,
        transform=ax.transAxes, fontsize=8,
        verticalalignment="top", horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("histograma_idades.png", dpi=150)
    plt.close()
    logger.info("histograma_idades.png salvo.")

    logger.info("Gráficos temporais gerados com sucesso.")


def plot_state_ranking(df: pd.DataFrame) -> None:
    """
    Gera um gráfico de pizza com a distribuição de notificações por estado (Top 10).

    Análise esperada:
      - Estados mais populosos e com maior densidade urbana (SP, RJ, MG)
        tendem a concentrar o maior volume absoluto de notificações.
      - Regiões Sudeste e Nordeste historicamente lideram os registros,
        refletindo clima favorável ao vetor e infraestrutura de saneamento
        ainda deficiente em parte do território.
      - A fatia "Outros" representa estados com menor volume individual,
        mas que somados podem ser relevantes epidemiologicamente.
    """
    plt.style.use("default")

    df_plot = df.copy()
    df_plot["estado_nome"] = df_plot["sg_uf_not"].astype(str).map(MAPEAMENTO_UFS)
    df_plot["estado_nome"] = df_plot["estado_nome"].fillna(df_plot["sg_uf_not"])

    state_counts = df_plot["estado_nome"].value_counts()

    limit = 10
    if len(state_counts) > limit:
        top_states = state_counts.head(limit)
        others_sum = state_counts.iloc[limit:].sum()
        final_counts = pd.concat([top_states, pd.Series({"Outros": others_sum})])
    else:
        final_counts = state_counts

    labels_lista = [str(label) for label in final_counts.index.tolist()]
    valores = np.array(final_counts.values, dtype=float)

    fig, ax = plt.subplots(figsize=(10, 10))

    cores = plt.cm.tab20.colors[: len(final_counts)]

    wedges, texts, autotexts = ax.pie(
        valores,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        pctdistance=0.82,
        explode=[0.05 if i < 3 else 0 for i in range(len(final_counts))],
    )

    plt.setp(autotexts, size=9, color="white", weight="bold")

    ax.set_title(
        "Distribuição de Notificações por Estado (Top 10)",
        fontsize=16, fontweight="bold", pad=20,
    )
    ax.axis("equal")

    ax.legend(
        wedges,
        labels_lista,
        title="Estados",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10,
    )

    # Estatísticas do ranking (pandas)
    pct = (valores / valores.sum() * 100).round(1)
    texto = (
        f"Top 3 concentram {pct[:3].sum():.1f}% dos casos\n"
        f"1º {labels_lista[0]}: {pct[0]:.1f}%\n"
        f"2º {labels_lista[1]}: {pct[1]:.1f}%\n"
        f"3º {labels_lista[2]}: {pct[2]:.1f}%"
    )
    fig.text(
        0.5, 0.01, texto,
        ha="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("casos_por_estado_pizza.png", bbox_inches="tight", dpi=150)
    plt.close()
    logger.info("casos_por_estado_pizza.png salvo.")