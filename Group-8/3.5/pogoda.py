import requests
def pogoda(lat = '43.2049',lon = '76.9049'):
    lat = str(lat)
    lon = str(lon)
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,rain,weather_code,wind_speed_10m&wind_speed_unit=ms&timezone=Europe%2FMoscow&forecast_days=1'

    r = requests.get(url).json()['current']
    temp = r['temperature_2m']
    wind = r['wind_speed_10m']
    rain = bool(r['rain'])
    ans = f'Температура: {temp} °C, \nСкорость ветра: {wind} м/с,\nДождь: {rain}'
    return ans