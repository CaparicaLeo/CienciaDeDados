import logging
import sys

import api_service
import transform_service
import model_service
import viz_service


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("main")


def _resumo(resultados):
    logger.info("=" * 60)
    logger.info("RESUMO DAS METRICAS")
    logger.info("=" * 60)

    for r in resultados:
        nome = r["modelo"]
        logger.info("--- %s ---", nome)
        if r["tipo"] == "classificacao":
            logger.info("  Acuracia:  %.4f", r["accuracy"])
            logger.info("  Precision: %.4f", r["precision"])
            logger.info("  Recall:    %.4f", r["recall"])
            logger.info("  F1-Score:  %.4f", r["f1"])
            logger.info("  F1-Macro:  %.4f", r.get("f1_macro", 0))
            logger.info("  ROC-AUC:   %.4f", r.get("roc_auc", 0))
        elif r["tipo"] == "regressao":
            logger.info("  R²:    %.4f", r["r2"])
            logger.info("  RMSE:  %.2f", r.get("rmse", 0))
        logger.info("")


def main():
    logger.info("=" * 60)
    logger.info("INICIANDO PIPELINE DE DENGUE")
    logger.info("=" * 60)

    # Etapa 1: Extracao
    logger.info("\n>>> ETAPA 1/4: EXTRACAO (API DATASUS)")
    api_service.run_extraction()

    # Etapa 2: Transformacao
    logger.info("\n>>> ETAPA 2/4: TRANSFORMACAO")
    df, df_agg_semana = transform_service.run_transform()

    # Etapa 3: Modelagem
    logger.info("\n>>> ETAPA 3/4: MODELAGEM")
    resultados = model_service.run_models(df, df_agg_semana)

    # Etapa 4: Visualizacao
    logger.info("\n>>> ETAPA 4/4: VISUALIZACAO")
    viz_service.run_viz(df, resultados)

    # Resumo final
    _resumo(resultados)

    logger.info("=" * 60)
    logger.info("PIPELINE FINALIZADO COM SUCESSO")
    logger.info("=" * 60)

    # Exibe resumo no terminal
    print("\n" + "=" * 60)
    print("RESUMO DAS METRICAS")
    print("=" * 60)
    for r in resultados:
        print(f"\n--- {r['modelo']} ---")
        if r["tipo"] == "classificacao":
            print(f"  Acuracia:  {r['accuracy']:.4f}")
            print(f"  Precision: {r['precision']:.4f}")
            print(f"  Recall:    {r['recall']:.4f}")
            print(f"  F1-Score:  {r['f1']:.4f}")
            print(f"  F1-Macro:  {r.get('f1_macro', 0):.4f}")
            print(f"  ROC-AUC:   {r.get('roc_auc', 0):.4f}")
        elif r["tipo"] == "regressao":
            print(f"  R²:    {r['r2']:.4f}")
            print(f"  RMSE:  {r.get('rmse', 0):.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
