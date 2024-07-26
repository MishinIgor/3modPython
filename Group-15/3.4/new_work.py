import requests

r = requests.get('https://goweather.herokuapp.com/weather/Moscow')
print(r.json())
temp = r.json()['temperature']
wind = r.json()['wind']
print(f'Погода в москве; температура: {temp}, Ветер: {wind}')