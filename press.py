import datetime as dt
import json

with open('plate.json', 'r') as file:
    data = json.load(file)

def default_pressing_mode(mode: dict, time=dt.datetime.now()):
    name = mode['name']
    start_heat = time
    time += dt.timedelta(minutes=mode['heat'])

    start_pressing = time
    time += dt.timedelta(minutes=mode['pressing'])

    start_cooler = time
    time += dt.timedelta(minutes=mode['air_cooling'])

    start_water = time
    time += dt.timedelta(minutes=mode['winter_water_cooling'])

    end_pressing = time

    return f'Название: {name}, Прогрев: {start_heat}, Начало прессования: {start_pressing}, Охлождение: {start_cooler}, Водяное: {start_water}, Конец прессования: {end_pressing}'

time = dt.timedelta(hours=16, minutes=50)

print(default_pressing_mode(data['thin_plates']['BV-30'], time))