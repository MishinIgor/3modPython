import requests
from transliterate import translit
city = 'Moscow'
cityen = translit(city, language_code='ru', reversed=True)
r = requests.get(f'https://goweather.herokuapp.com/weather/{cityen}')
wind = r.json()['wind']
wind = wind.split()
wind = int(wind[0])
wind = wind*1000/3600
print(wind)
