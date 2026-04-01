import requests as req
import csv
import time

base_url = 'https://apidadosabertos.saude.gov.br/arboviroses/dengue'
headers = {'accept': 'application/json'}
limit = 20

with open('dados_dengue.csv', 'w', newline='', encoding='utf-8') as file:
    writer = None
    
    for ano in range(2015,2026):
        offset = 0
        
        while True:
            print(f'Buscando ano {ano} | Offset: {offset}')
            
            params = {
                'nu_ano': ano,
                'limit': limit, 
                'offset': offset
            }
            
            response = req.get(base_url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"Erro:{response.status_code} no ano {ano}. Encerrando o ano.")
                break
            
            response_json = response.json()
            
            dados = response_json.get('parametros', [])
            
            if not dados:
                break
                
            if writer is None:
                colunms = dados[0].keys()
                writer = csv.DictWriter(file, fieldnames=colunms)
                writer.writeheader()
                
            for item in dados:
                writer.writerow(item)
            
            offset += 1
            
            if len(dados) < limit:
                break
            
            time.sleep(0.5)
            
print('Extracao Concluída')
                