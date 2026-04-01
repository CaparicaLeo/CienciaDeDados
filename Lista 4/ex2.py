import requests
from bs4 import BeautifulSoup

# 1. Obter o HTML da página
url = "https://exemplo.com"
resposta = requests.get(url)

# 2. Criar o objeto BeautifulSoup (parsear o HTML)
soup = BeautifulSoup(resposta.text, "html.parser")

# 3. Extrair elementos desejados
# find() → retorna o PRIMEIRO elemento encontrado
primeiro_h2 = soup.find("h2")

# find_all() → retorna TODOS os elementos em uma lista
todos_h2 = soup.find_all("h2")

# 4. Iterar e usar os dados
for titulo in todos_h2:
    print(titulo.text.strip())  # .text extrai o texto puro; .strip() remove espaços