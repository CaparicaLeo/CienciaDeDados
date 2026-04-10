import requests

url = "https://api.github.com/search/repositories?q=topic:data-science"
data = requests.get(url).json()

for repo in data['items']:
    print(f"Nome: {repo['name']} | URL: {repo['html_url']}")