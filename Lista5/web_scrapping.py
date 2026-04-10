import requests
from bs4 import BeautifulSoup

url = 'https://pt.wikipedia.org/wiki/Python'

response = requests.get(url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

print(f"--- Títulos encontrados na página: {url} ---\n")
for h2 in soup.find_all('h2'):
    texto = h2.get_text(strip=True).replace('[editar]', '')
    if texto:
        print(f"Seção: {texto}")