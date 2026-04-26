"""
Pipeline de Dados de Dengue — Gov.br → MySQL
=============================================
Orquestra as etapas de coleta, transformação, persistência e visualização.

Execução manual:
    python main.py

Agendamento (Linux/macOS — cron):
    Abra o crontab com: crontab -e
    Adicione a linha abaixo para rodar todo dia às 03:00:
        0 3 * * * /usr/bin/python3 /caminho/para/main.py >> /var/log/dengue_pipeline.log 2>&1

Agendamento (Windows — Task Scheduler):
    1. Abra o Agendador de Tarefas (taskschd.msc)
    2. Criar Tarefa Básica → Nome: "Pipeline Dengue"
    3. Gatilho: Diário, às 03:00
    4. Ação: Iniciar programa
       Programa: python
       Argumentos: C:\\caminho\\para\\main.py
       Iniciar em: C:\\caminho\\para\\
"""

import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import api_service
from transform_service import transform_data
from db_service import save_to_db, get_cases_by_state, get_cases_statistics
from viz_service import plot_state_ranking, generate_charts

# ── Configuração de Logging ──────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_filename = LOG_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),  # grava em arquivo
        logging.StreamHandler(sys.stdout),                    # exibe no terminal
    ],
)

# DEBUG apenas no módulo de coleta — investiga resposta vazia do ano 2015
logging.getLogger("api_service").setLevel(logging.DEBUG)

logger = logging.getLogger("pipeline")


def run_pipeline() -> None:
    inicio = time.time()
    logger.info("=" * 60)
    logger.info("PIPELINE DE DADOS DE DENGUE — INÍCIO")
    logger.info("=" * 60)

    try:
        # ── Passo 1: Coleta ──────────────────────────────────────────────────
        logger.info("[1/5] Coletando dados da API do DATASUS...")
        api_service.run_extraction()

        # ── Passo 2: Transformação ───────────────────────────────────────────
        logger.info("[2/5] Transformando e limpando os dados...")
        df_clean = transform_data("dados_dengue.csv")

        # ── Passo 3: Banco de Dados ──────────────────────────────────────────
        logger.info("[3/5] Persistindo no MySQL (com transação)...")
        save_to_db(df_clean)

        # ── Passo 4: Análise Exploratória ────────────────────────────────────
        logger.info("[4/5] Executando análise exploratória...")

        df_uf = get_cases_by_state()
        logger.info("\n%s\nRANKING DE ESTADOS (Top 10)\n%s\n%s\n%s",
                    "=" * 40,
                    "=" * 40,
                    df_uf.head(10).to_string(index=False),
                    "=" * 40)

        stats = get_cases_statistics()
        logger.info(
            "Estatísticas anuais — Média: %.1f | Máx: %d | Mín: %d",
            stats["media_anual"], stats["max_anual"], stats["min_anual"],
        )

        # ── Passo 5: Visualizações ───────────────────────────────────────────
        logger.info("[5/5] Gerando gráficos...")
        generate_charts(df_clean)      # barras (anual) + linha (sazonalidade)
        plot_state_ranking(df_clean)   # pizza (distribuição por estado)

        # ── Relatório Final ──────────────────────────────────────────────────
        duracao = time.time() - inicio
        logger.info("=" * 60)
        logger.info("PIPELINE FINALIZADO COM SUCESSO em %.1fs", duracao)
        logger.info("Arquivos gerados:")
        logger.info("  Log:      %s", log_filename)
        logger.info("  Gráfico 1: casos_por_ano.png")
        logger.info("  Gráfico 2: histograma_idades.png")
        logger.info("  Gráfico 3: casos_por_estado_pizza.png")
        logger.info("=" * 60)

    except FileNotFoundError as e:
        logger.error("Arquivo não encontrado: %s", e)
        sys.exit(1)
    except Exception as e:
        duracao = time.time() - inicio
        logger.critical("PIPELINE FALHOU após %.1fs — Erro: %s", duracao, e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()