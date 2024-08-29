import requests


def requisicao_get(url):
    response = requests.get(url)
    return response.json()


print(requisicao_get('https://api.github.com/users/Essence999'))
