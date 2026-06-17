import requests as req
import csv
import time
import logging

logger = logging.getLogger(__name__)


def run_extraction():
    """
    Coleta dados de dengue da API pública do DATASUS (Gov.br).
    Salva os resultados em 'dados_dengue.csv'.
    Cobre os anos de 2015 a 2025, com até 2000 registros por ano.
    """
    base_url = "https://apidadosabertos.saude.gov.br/arboviroses/dengue"
    headers = {"accept": "application/json"}
    limit = 20          # Máximo permitido pela documentação da API
    max_registros = 2000
    max_paginas = max_registros // limit

    logger.info("Iniciando extração da API do DATASUS...")

    total_registros = 0

    try:
        with open("dados_dengue.csv", "w", newline="", encoding="utf-8") as file:
            writer = None

            for ano in range(2015, 2026):
                offset = 0
                registros_ano = 0

                while offset < max_paginas:
                    logger.debug(
                        "Ano %d | Offset: %d | ~%d registros coletados no ano",
                        ano, offset, offset * limit,
                    )

                    params = {"nu_ano": ano, "limit": limit, "offset": offset}

                    try:
                        response = req.get(
                            base_url, headers=headers, params=params, timeout=30
                        )
                        response.raise_for_status()
                    except req.exceptions.Timeout:
                        logger.warning("Timeout no ano %d, offset %d. Pulando página.", ano, offset)
                        break
                    except req.exceptions.HTTPError as e:
                        logger.error("Erro HTTP %s no ano %d. Pulando ano.", e, ano)
                        break
                    except req.exceptions.RequestException as e:
                        logger.error("Erro de rede no ano %d: %s", ano, e)
                        break

                    response_json = response.json()

                    # DEBUG: loga as chaves retornadas para identificar formato inesperado
                    if offset == 0:
                        logger.debug(
                            "Ano %d — chaves na resposta: %s | status: %d",
                            ano, list(response_json.keys()), response.status_code,
                        )

                    # A API pode retornar dados em chaves diferentes
                    dados = response_json.get("resultados") or response_json.get("parametros") or []

                    if not dados:
                        logger.warning(
                            "Ano %d, offset %d: resposta sem dados. "
                            "Chaves recebidas: %s | Conteúdo: %s",
                            ano, offset,
                            list(response_json.keys()),
                            str(response_json)[:300],  # limita para não poluir o log
                        )
                        break

                    if writer is None:
                        colunas = dados[0].keys()
                        writer = csv.DictWriter(file, fieldnames=colunas)
                        writer.writeheader()
                        logger.info("Header CSV criado com colunas: %s", list(colunas))

                    for item in dados:
                        writer.writerow(item)

                    registros_ano += len(dados)
                    offset += 1

                    if len(dados) < limit:
                        break

                    time.sleep(0.3)

                logger.info("Ano %d: %d registros coletados.", ano, registros_ano)
                total_registros += registros_ano

    except IOError as e:
        logger.critical("Não foi possível criar o arquivo CSV: %s", e)
        raise

    logger.info(
        "Extração finalizada. Total: %d registros salvos em 'dados_dengue.csv'.",
        total_registros,
    )