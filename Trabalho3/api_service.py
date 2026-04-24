import requests as req
import csv
import time

def run_extraction():
    base_url = 'https://apidadosabertos.saude.gov.br/arboviroses/dengue'
    headers = {'accept': 'application/json'}
    limit = 20 # Máximo permitido pela documentação
    max_registros = 2000
    max_paginas = max_registros // limit # Isso resulta em 100 páginas

    with open('dados_dengue.csv', 'w', newline='', encoding='utf-8') as file:
        writer = None
        
        for ano in range(2015, 2026):
            # Reinicia o offset para cada ano
            offset = 0
            
            # O loop roda enquanto não atingir a página 100 (2000 registros)
            while offset < max_paginas:
                print(f'Ano {ano} | Página (Offset): {offset} | Aprox. {offset * limit} registros')
                
                params = {
                    'nu_ano': ano,
                    'limit': limit, 
                    'offset': offset
                }
                
                response = req.get(base_url, headers=headers, params=params)
                
                if response.status_code != 200:
                    print(f"Erro {response.status_code} no ano {ano}. Pulando...")
                    break
                
                response_json = response.json()
                # Verifique se a chave é 'resultados' ou 'parametros' conforme o retorno real
                dados = response_json.get('resultados', response_json.get('parametros', []))
                
                if not dados:
                    break
                    
                if writer is None:
                    colunms = dados[0].keys()
                    writer = csv.DictWriter(file, fieldnames=colunms)
                    writer.writeheader()
                    
                for item in dados:
                    writer.writerow(item)
                
                # Incrementa de 1 em 1, pois offset aqui é o NÚMERO DA PÁGINA
                offset += 1
                
                # Se a página veio incompleta, significa que os dados do ano acabaram
                if len(dados) < limit:
                    break
                
                time.sleep(0.3)
                
    print('Extração finalizada com o limite de 2000 registros por ano.')