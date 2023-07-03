import speech_recognition
import pyttsx3
import requests
import winsound
from config2 import open_weather_token

sr = speech_recognition.Recognizer()    # создаем объект класса reocgnize
sr.pause_threshold = 0.5        # отвечает за время которое наш текст будет принят


def get_weather(city, open_weather_token):
    code_to_smile = {                   # создали словарь, где значения переводят на русский ключи
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric" # запросили апи о погоде
        )
        data = r.json()                         # записали json файл

        city = data["name"]                     # достаем город из json
        cur_weather = data["main"]["temp"]      # достаем температуру из Json

        weather_description = data["weather"][0]["main"]    # взяли описание погоды из json
        if weather_description in code_to_smile:        # если описание совпавадает с ключом словаря, то присваиваем значение ключа
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"     # если не нашлось, присваиваем ошибку

        d['погода'] = f'Погода в городе: {city} Температура: {cur_weather}C° {wd.split()[0]}'   # добавили в словарь ответов запись о погоде
        print(d['погода'] + wd.split()[1])  # Вывели
        answer('погода')                    # Ответ голосового помощника

    except Exception as ex:
        print(ex)
        print("Проверьте название города")          # если в блоке выше будет ошибка выводим следующее:


def answer(a):
    engine = pyttsx3.init()

    engine.setProperty('rate', 200)         # скорость речи
    engine.setProperty('volume', 1)         # громкость ответа

    engine.say(d[a])                        # что будет говорить, выбираем из словаря
    return engine.runAndWait()


def listen_command():
    """This functional will return the recognized command"""

    try:

        with speech_recognition.Microphone() as mic:                # подключаем микрофон
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)   # подавление внешнего шума
            audio = sr.listen(source=mic)                           # запускаем прослушивание
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()     # что услышал голосовой помощник

        return query        # возвращаем
    except speech_recognition.UnknownValueError:
        return 'Damn...'


def greeting():
    """Greeting function"""

    return 'Привет Никитос!'        # Приветствие


def create_task():
    """Create a todo task"""
    print('Что добавим в список дел?')

    query = listen_command()

    with open('todo-list.txt', 'a') as file:        # записываем в файл что хотим добавить
        file.write(f'{query}\n')
    answer('добавлено')
    return f'Задача {query} добавлена успешно!'


def play_music():
    """Play a mp3 file"""

    filename = 'C:\\Users\\zenin\\Desktop\\po_restoranam (online-audio-converter.com).wav'      # путь к музыке
    winsound.PlaySound(filename, winsound.SND_ASYNC + winsound.SND_LOOP)    # запуск музыки
    input('Чтобы остановить музыку, нажмите на любую клавишу')
    winsound.PlaySound(None, winsound.SND_ASYNC)    # пауза


def main():
    answer('старт')
    print('Я тебя слушаю')
    query = listen_command()
    while query != 'стоп':
        if query == 'привет':
            answer(query)
            print(greeting())
        elif query == 'добавить задачу':
            answer(query)
            print(create_task())
        elif query == 'включи музыку':
            answer(query)
            play_music()
        elif query == 'погода':
            get_weather('moscow', open_weather_token)
        else:
            print('Я вас не понял!')
        query = listen_command()
    else:
        answer('стоп')


if __name__ == '__main__':
    d = {'привет': 'Привет, я голосовой помощник Жук, я готов выполнять твои команды',  # словарь с ответами
         'включи музыку': 'включаю музыку',
         'добавить задачу': 'Какую задачу вы хотите добавить?',
         'добавлено': 'задача успешно добавлена',
         'старт': 'я тебя слушаю',
         'стоп': 'я завершаю свою работу'
         }
    main()
