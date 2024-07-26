import requests
def weather_info(lat,lon):
    r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={str(lat)}&longitude={str(lon)}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,rain,weather_code,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=weather_code,sunrise,sunset,precipitation_sum,rain_sum,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant&wind_speed_unit=ms&timezone=Europe%2FMoscow&forecast_days=1')
    info = r.json()['current']
    code_weather = {
        "0":{
            "день":{
                "описание": "Солнечный",
"изображение":"http://openweathermap.org/img/wn/01d@2x.png "
            },
"ночь":{
                "описание": "Четкий",
"изображение":"http://openweathermap.org/img/wn/01n@2x.png "
            }
        },
        "1":{
            "день":{
                "описание":"В основном солнечно",
"изображение":"http://openweathermap.org/img/wn/01d@2x.png "
            },
"ночь":{
                "описание": "В основном ясно",
                "изображение":"http://openweathermap.org/img/wn/01n@2x.png"
            }
        },
        "2":{
            "день":{
                "описание":"Переменная облачность",
"изображение":"http://openweathermap.org/img/wn/02d@2x.png "
            },
"ночь":{
                "описание":"Переменная облачность",
"изображение":"http://openweathermap.org/img/wn/02n@2x.png"
            }
        },
        "3":{
            "день":{
                "описание": "Облачно",
"изображение":"http://openweathermap.org/img/wn/03d@2x.png "
            },
"ночь":{
                "описание": "Облачно",
"изображение":"http://openweathermap.org/img/wn/03n@2x.png "
            }
        },
        "45":{
            "день":{
                "описание": "Туманно",
"изображение":"http://openweathermap.org/img/wn/50d@2x.png "
            },
"ночь":{
                "описание": "Туманно",
"изображение":"http://openweathermap.org/img/wn/50n@2x.png "
            }
        },
        "48":{
            "день":{
                "описание": "Туман инея",
                "изображение":"http://openweathermap.org/img/wn/50d@2x.png "
            },
"ночь":{
                "описание": "Туман инея",
"изображение":"http://openweathermap.org/img/wn/50n@2x.png "
            }
        },
        "51":{
            "день":{
                "описание":"Легкая морось",
"изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Легкая морось",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png "
            }
        },
        "53":{
            "день":{
                "описание":"Моросящий дождь",
"изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Моросящий дождь",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png "
            }
        },
        "55":{
            "день":{
                "описание":"Сильный моросящий дождь",
"изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Сильный моросящий дождь",
                "изображение":"http://openweathermap.org/img/wn/09n@2x.png"
            }
        },
        "56":{
            "день":{
                "описание":"Легкая моросящая изморось",
"изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Легкая моросящая изморось",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png"
            }
        },
        "57":{
            "день":{
                "описание":"Моросящий дождь",
                "изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Моросящий дождь",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png "
            }
        },
        "61":{
            "день":{
                "описание": "Легкий дождь",
"изображение":"http://openweathermap.org/img/wn/10d@2x.png "
            },
"ночь":{
                "описание": "Легкий дождь",
"изображение":"http://openweathermap.org/img/wn/10n@2x.png "
            }
        },
        "63":{
            "день":{
                "описание": "Дождь",
"изображение":"http://openweathermap.org/img/wn/10d@2x.png "
            },
"ночь":{
                "описание": "Дождь",
"изображение":"http://openweathermap.org/img/wn/10n@2x.png "
            }
        },
        "65":{
            "день":{
                "описание": "Сильный дождь",
"изображение":"http://openweathermap.org/img/wn/10d@2x.png "
            },
"ночь":{
                "описание":"Сильный дождь",
                "изображение":"http://openweathermap.org/img/wn/10n@2x.png"
            }
        },
        "66":{
            "день":{
                "описание": "Легкий ледяной дождь",
"изображение":"http://openweathermap.org/img/wn/10d@2x.png "
            },
"ночь":{
                "описание":"Легкий ледяной дождь",
"изображение":"http://openweathermap.org/img/wn/10n@2x.png"
            }
        },
        "67":{
            "день":{
                "описание": "Ледяной дождь",
                "изображение":"http://openweathermap.org/img/wn/10d@2x.png "
            },
"ночь":{
                "описание": "Ледяной дождь",
"изображение":"http://openweathermap.org/img/wn/10n@2x.png "
            }
        },
        "71":{
            "день":{
                "описание": "Легкий снегопад",
"изображение":"http://openweathermap.org/img/wn/13d@2x.png "
            },
"ночь":{
                "описание": "Легкий снегопад",
"изображение":"http://openweathermap.org/img/wn/13n@2x.png "
            }
        },
        "73":{
            "день":{
                "описание": "Снег",
"изображение":"http://openweathermap.org/img/wn/13d@2x.png "
            },
"ночь":{
                "описание": "Снег",
"изображение":"http://openweathermap.org/img/wn/13n@2x.png "
            }
        },
        "75":{
            "день":{
                "описание":"Сильный снегопад",
"изображение":"http://openweathermap.org/img/wn/13d@2x.png "
            },
"ночь":{
                "описание":"Сильный снегопад",
                "изображение":"http://openweathermap.org/img/wn/13n@2x.png"
            }
        },
        "77":{
            "день":{
                "описание": "Снежные крупинки",
"изображение":"http://openweathermap.org/img/wn/13d@2x.png "
            },
"ночь":{
                "описание":"Снежинки",
"изображение":"http://openweathermap.org/img/wn/13n@2x.png"
            }
        },
        "80":{
            "день":{
                "описание": "Легкие дожди",
"изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание": "Легкие дожди",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png "
            }
        },
        "81":{
            "день":{
                "описание":"Душевые кабины",
"изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Душевые кабины",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png "
            }
        },
        "82":{
            "день":{
                "описание":"Сильные ливни",
                "изображение":"http://openweathermap.org/img/wn/09d@2x.png "
            },
"ночь":{
                "описание":"Сильные ливни",
"изображение":"http://openweathermap.org/img/wn/09n@2x.png "
            }
        },
        "85":{
            "день":{
                "описание": "Небольшой снегопад",
"изображение":"http://openweathermap.org/img/wn/13d@2x.png "
            },
"ночь":{
                "описание": "Небольшой снегопад",
"изображение":"http://openweathermap.org/img/wn/13n@2x.png "
            }
        },
        "86":{
            "день":{
                "описание":"Снежные дожди",
"изображение":"http://openweathermap.org/img/wn/13d@2x.png "
            },
"ночь":{
                "описание":"Снежные дожди",
"изображение":"http://openweathermap.org/img/wn/13n@2x.png "
            }
        },
        "95":{
            "день":{
                "описание": "Гроза",
"изображение":"http://openweathermap.org/img/wn/11d@2x.png "
            },
"ночь":{
                "описание": "Гроза",
                "изображение":"http://openweathermap.org/img/wn/11n@2x.png"
            }
        },
        "96":{
            "день":{
                "описание": "Небольшие Грозы С Градом",
"изображение":"http://openweathermap.org/img/wn/11d@2x.png "
            },
"ночь":{
                "описание":"Небольшие Грозы С Градом",
"изображение":"http://openweathermap.org/img/wn/11n@2x.png"
            }
        },
        "99":{
            "день":{
                "описание": "Гроза С Градом",
                "изображение":"http://openweathermap.org/img/wn/11d@2x.png "
            },
"ночь":{
                "описание": "Гроза с Градом",
"изображение":"http://openweathermap.org/img/wn/11n@2x.png "
            }
        }
    }
    lst = ['С', "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    wind_dir = lst[info['wind_direction_10m'] //45]
    temp = info['temperature_2m']
    wind_speed = info['wind_speed_10m']
    wind_gusts = info['wind_gusts_10m']
    clouds = code_weather[str(info['weather_code'])]['день']['описание']
    relative = info['relative_humidity_2m']
    all_info = f'''Температура воздуха: {temp};
    Скорость ветра: {wind_speed};
    Порывы ветра: {wind_gusts};
    Облачность: {clouds};
    Влажность: {relative};
    Направление ветра: {wind_dir}'''
    return all_info
