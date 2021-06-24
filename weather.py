import requests


# ключ для доступа к сервису openweather.org
TOKEN = "2de2066e26914e2c3d870fd02592dba3"


def get_current_weather(city):
    """
    Функция, возвращающая текущую погоду в городе.
    """
    try:
        # запрос к сайту, используя необходимые параметры
        # q - название города
        # units - отображение тем-ры в Цельсиях
        # APPID - токен
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': TOKEN})
        # Результат запроса в json-формате
        data = res.json()
        # Шаблон вывода
        info = 'Текущая погода в городе {}:\n\n' \
               '- {}\n' \
               '- Температура воздуха: {}°С\n' \
               '- Влажность воздуха: {}%\n' \
               '- Скорость ветра: {} м/с\n'.format(city, data['weather'][0]['description'].capitalize(),
                                                 data['main']['temp'], data['main']['humidity'], data['wind']['speed'])
        # вытаскиваем необходимые сведения из словаря data
        return info
    # если возникла ошибка
    except Exception as e:
        print("Exception (find):", e)
        return 'Ошибка запроса! Погоды для данного города не найдено!'


def get_forecast_weather(city):
    """
    Функция, выводящая прогноз на несколько дней.
    """
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast?",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': TOKEN})
        data = res.json()
        # словари для определенного объема информации
        temperatures = {}  # словарь для температур
        weather = {}  # словарь для текстового описания погоды
        # проходимся по каждой дате из списка прогнозов
        for forecast in data['list']:
            # дата в общепринятом виде
            date = forecast['dt_txt'].split()[0]
            # добавляем дату в оба словаря - значением ключей будет множество
            if date not in temperatures:
                temperatures[date] = set()
            if date not in weather:
                weather[date] = set()
            # добавляем в множества информацию
            temperatures[date].add(forecast['main']['temp'])
            weather[date].add(forecast['weather'][0]['description'])
        res = 'Прогноз погоды в городе {}:\n\n'.format(city)
        # собираем ответ функции
        for date in temperatures.keys():
            res += '{}\n- В течение дня: {}\n- Максимальная температура: {}°С\n- Минимальная ' \
                   'температура: {}°С\n\n'.format('/'.join(reversed(date.split('-'))), ', '.join(weather[date]),
                                                  max(temperatures[date]), min(temperatures[date]))
    except Exception as e:
        # если что-то пошло не так
        print("Exception (find):", e)
        return 'Ошибка запроса! Погоды для данного города не найдено!'
    return res

