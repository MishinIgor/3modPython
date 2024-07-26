import requests
def info_weather(lat=43.2049,lon=76.9049):
    WMO = {
  "0":{
  "день":{
  "description":"Солнечно",
  "image":"http://openweathermap.org/img/wn/01d@2x.png"
  },
  "ночь":{
  "description":"Очистить",
  "image":"http://openweathermap.org/img/wn/01n@2x.png"
  }
  },
  "1":{
  "день":{
  "description":"Преимущественно солнечно",
  "image":"http://openweathermap.org/img/wn/01d@2x.png"
  },
  "ночь":{
  "description":"В основном ясно",
  "image":"http://openweathermap.org/img/wn/01n@2x.png"
  }
  },
  "2":{
  "день":{
  "description":"Переменная облачность",
  "image":"http://openweathermap.org/img/wn/02d@2x.png"
  },
  "ночь":{
  "description":"Переменная облачность",
  "image":"http://openweathermap.org/img/wn/02n@2x.png"
  }
  },
  "3":{
  "день":{
  "description":"Облачно",
  "image":"http://openweathermap.org/img/wn/03d@2x.png"
  },
  "ночь":{
  "description":"Облачно",
  "image":"http://openweathermap.org/img/wn/03n@2x.png"
  }
  },
  "45":{
  "день":{
  "description":"Туманно",
  "image":"http://openweathermap.org/img/wn/50d@2x.png"
  },
  "ночь":{
  "description":"Туманно",
  "image":"http://openweathermap.org/img/wn/50n@2x.png"
  }
  },
  "48":{
  "день":{
  "description":"Инейный туман",
  "image":"http://openweathermap.org/img/wn/50d@2x.png"
  },
  "ночь":{
  "description":"Инейный туман",
  "image":"http://openweathermap.org/img/wn/50n@2x.png"
  }
  },
  "51":{
  "день":{
  "description":"Легкий дождь",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Легкий дождь",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "53":{
  "день":{
  "description":"Дождь",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Дождь",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "55":{
  "день":{
  "description":"Сильный дождь",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Сильный дождь",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "56":{
  "день":{
  "description":"Легкий ледяной дождь",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Легкий ледяной дождь",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "57":{
  "день":{
  "description":"Ледяной дождь",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Ледяной дождь",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "61":{
  "день":{
  "description":"Легкий дождь",
  "image":"http://openweathermap.org/img/wn/10d@2x.png"
  },
  "ночь":{
  "description":"Легкий дождь",
  "image":"http://openweathermap.org/img/wn/10n@2x.png"
  }
  },
  "63":{
  "день":{
  "description":"Дождь",
  "image":"http://openweathermap.org/img/wn/10d@2x.png"
  },
  "ночь":{
  "description":"Дождь",
  "image":"http://openweathermap.org/img/wn/10n@2x.png"
  }
  },
  "65":{
  "день":{
  "description":"Сильный дождь",
  "image":"http://openweathermap.org/img/wn/10d@2x.png"
  },
  "ночь":{
  "description":"Сильный дождь",
  "image":"http://openweathermap.org/img/wn/10n@2x.png"
  }
  },
  "66":{
  "день":{
  "description":"Легкий ледяной дождь",
  "image":"http://openweathermap.org/img/wn/10d@2x.png"
  },
  "ночь":{
  "description":"Легкий ледяной дождь",
  "image":"http://openweathermap.org/img/wn/10n@2x.png"
  }
  },
  "67":{
  "день":{
  "description":"Ледяной дождь",
  "image":"http://openweathermap.org/img/wn/10d@2x.png"
  },
  "ночь":{
  "description":"Ледяной дождь",
  "image":"http://openweathermap.org/img/wn/10n@2x.png"
  }
  },
  "71":{
  "день":{
  "description":"Легкий снег",
  "image":"http://openweathermap.org/img/wn/13d@2x.png"
  },
  "ночь":{
  "description":"Легкий снег",
  "image":"http://openweathermap.org/img/wn/13n@2x.png"
  }
  },
  "73":{
  "день":{
  "description":"Снег",
  "image":"http://openweathermap.org/img/wn/13d@2x.png"
  },
  "ночь":{
  "description":"Снег",
  "image":"http://openweathermap.org/img/wn/13n@2x.png"
  }
  },
  "75":{
  "день":{
  "description":"Сильный снегопад",
  "image":"http://openweathermap.org/img/wn/13d@2x.png"
  },
  "ночь":{
  "description":"Сильный снегопад",
  "image":"http://openweathermap.org/img/wn/13n@2x.png"
  }
  },
  "77":{
  "день":{
  "description":"Снежные зерна",
  "image":"http://openweathermap.org/img/wn/13d@2x.png"
  },
  "ночь":{
  "description":"Снежные зерна",
  "image":"http://openweathermap.org/img/wn/13n@2x.png"
  }
  },
  "80":{
  "день":{
  "description":"Легкие ливни",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Легкие ливни",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "81":{
  "день":{
  "description":"Душ",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Душ",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "82":{
  "день":{
  "description":"Сильный ливень",
  "image":"http://openweathermap.org/img/wn/09d@2x.png"
  },
  "ночь":{
  "description":"Сильный ливень",
  "image":"http://openweathermap.org/img/wn/09n@2x.png"
  }
  },
  "85":{
  "день":{
  "description":"Легкий снегопад",
  "image":"http://openweathermap.org/img/wn/13d@2x.png"
  },
  "ночь":{
  "description":"Легкий снегопад",
  "image":"http://openweathermap.org/img/wn/13n@2x.png"
  }
  },
  "86":{
  "день":{
  "description":"Снежные ливни",
  "image":"http://openweathermap.org/img/wn/13d@2x.png"
  },
  "ночь":{
  "description":"Снежные ливни",
  "image":"http://openweathermap.org/img/wn/13n@2x.png"
  }
  },
  "95":{
  "день":{
  "description":"Гроза",
  "image":"http://openweathermap.org/img/wn/11d@2x.png"
  },
  "ночь":{
  "description":"Гроза",
  "image":"http://openweathermap.org/img/wn/11n@2x.png"
  }
  },
  "96":{
  "день":{
  "description":"Небольшая гроза с градом",
  "image":"http://openweathermap.org/img/wn/11d@2x.png"
  },
  "ночь":{
  "description":"Небольшая гроза с градом",
  "image":"http://openweathermap.org/img/wn/11n@2x.png"
  }
  },
  "99":{
  "день":{
  "description":"Гроза с градом",
  "image":"http://openweathermap.org/img/wn/11d@2x.png"
  },
  "ночь":{
  "description":"Гроза с градом",
  "image":"http://openweathermap.org/img/wn/11n@2x.png"
  }
  }
}
  
    r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&wind_speed_unit=ms&timezone=Europe%2FMoscow&forecast_days=1')
    info = r.json()['current']
    day_or_night = ['ночь',"день"]
    wind_direction = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    weather_info = {
        'Температура воздуха': info['temperature_2m'],
        'Скорость ветра': info['wind_speed_10m'],
        'Порывы ветра': info['wind_gusts_10m'],
        "Относительная влажность": info['relative_humidity_2m'],
        "День/ночь": day_or_night[info['is_day']],
        "Описание": WMO[str(info['weather_code'])][day_or_night[info['is_day']]]['description'], 
        "Направление ветра": wind_direction[info['wind_direction_10m']//45]
    }
    all_info = ''
    for i,j in weather_info.items():
        all_info += f'{i}: {j};\n'
    return all_info
