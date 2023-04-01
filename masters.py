import datetime as dt
import json

with open('plate.json', 'r') as file:
    data = json.load(file)

def create_timetable(data, total, time, summer_or_winter, plate_size):
    """ Функция принимает json файл, количесво запрессовок и время начала.
        Должна вернуть список расписания """
    data = data[plate_size]
    
    out = list()
    for i in range(total):
        type_plate = int(input('Введите тип плиты. 0 - Б, 1 - В: '))
        name_plate = 'BV-' + input('Введите марку плиты (BV-*число*): ')

             
        if summer_or_winter == 'w':
            out.append(f'{data[name_plate]["name"][type_plate]} - {time} --- {time + dt.timedelta(minutes=data[name_plate]["winter_total_time"])}')
            time += dt.timedelta(minutes=data[name_plate]["winter_total_time"])
        else:
            out.append(f'{data[name_plate]["name"][type_plate]} - {time} --- {time + dt.timedelta(minutes=data[name_plate]["summer_total_time"])}')
            time += dt.timedelta(minutes=data[name_plate]["summer_total_time"])
        
        if plate_size == 'thin_plates':
               out.append('РАЗГРУЗКА 15 МИНУТ')
               time += dt.timedelta(minutes=15)
        else:
             out.append('РАЗГРУЗКА 5 МИНУТ')
             time += dt.timedelta(minutes=5)
             
    return out


time = dt.timedelta(hours=16, minutes=50)

k = create_timetable(data, 3, time, 'w', 'thin_plates')

for j in k:
     print(j)