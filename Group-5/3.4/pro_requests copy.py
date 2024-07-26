import requests
text = input('Введите слово: ')
r = requests.get(f'https://cataas.com/cat/says/{text}?json=true')
print(r.status_code)

