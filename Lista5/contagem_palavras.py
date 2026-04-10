import re
from collections import Counter

texto = open('arquivo.txt', 'r', encoding='utf-8').read().lower()
palavras = re.findall(r'\b\w+\b', texto)
for palavra, total in Counter(palavras).most_common(10):
    print(f"{palavra}: {total}")