import requests
from transliterate import translit
city = input('Введите город с большой буквы: ')
cityen = translit(city,language_code='ru',reversed=True)
rezult = ''
try:
    r = requests.get(f'https://goweather.herokuapp.com/weather/{cityen}')
    rezult = r.json()
    temp = rezult['temperature']
    wind = rezult['wind']
    wind = int(wind.split()[0])
    wind = str(round(wind*1000/3600,2)) +' м/c'
    rezult = f'Погода в городе {city}: Температура - {temp}, Скорость ветра - {wind}'
except Exception:
    rezult = 'Ввели некорректные данные'
    

print(rezult)