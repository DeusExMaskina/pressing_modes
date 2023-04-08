from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.lang import Builder

import datetime as dt
import json


Config.set('graphics', 'resizable', 0)
# Config.set('graphics', 'width', 400)
# Config.set('graphics', 'height', 600)
# Config.set('graphics', 'minimum_width', 200)
# Config.set('graphics', 'minimum_height', 400)

BTN_COLOR = [.39, .67, .82, 1]
BTN_COLOR_CLOSE = [.96, .19, .19, 1]
BTN_COLOR_CREATE = [.13, .78, 0, 1]


class MainScreen(Screen):
    pass


class ScheduleModesScreen(Screen):
    hour_input = ObjectProperty()
    minute_input = ObjectProperty()

    check_w = ObjectProperty()

    def get_size_plate(self):
        """ Берет размер плит (целое число) и создает кнопки для составление режима прессования """
        
        with open('plate.json', 'r') as file:
            self.data = json.load(file)

        window = ModalView(auto_dismiss=False)
        gl = GridLayout(cols=3, padding=10)

        gl.add_widget(Button(
            text='Назад',
            background_color=[.96, .19, .19, 1],
            on_press=window.dismiss
        ))

        for i in self.data:
            gl.add_widget(Button(
                text=i,
                on_press=self.get_modes
            ))

        window.add_widget(gl)
        window.open()

    
    def get_modes(self, *args):
        """ Берет из json время режимов прессования в минутах и выводит режимы в модальном окне """

        window = ModalView(auto_dismiss=False)

        with open('plate.json', 'r') as file:
            self.data = json.load(file)

        try:
            time = dt.timedelta(hours=int(self.hour_input.text), minutes=int(self.minute_input.text))
        except ValueError:
            time = dt.timedelta(hours=0, minutes=0)
        mark = args[0].text

        heat_start = time
        time += dt.timedelta(minutes=self.data[mark]["heat"])
        pressing_start = time
        time += dt.timedelta(minutes=self.data[mark]['pressing'])

        air_cooler_start = time
        time += dt.timedelta(minutes=self.data[mark]['air_cooling'])

        water_cooler_start = time
        if self.check_w.state == 'down':
            time += dt.timedelta(minutes=self.data[mark]['winter_water_cooling'])
        else:
            time += dt.timedelta(minutes=self.data[mark]['summer_water_cooling'])

        pressing_end = time

        name_label = Label(text=f'Размер: {str(mark)}', font_size=24)
        heat_label = Label(text=f'Прогрев: {str(heat_start)} - {str(pressing_start)}', font_size=24)
        pressing_label = Label(text=f'Прессование: {str(pressing_start)} - {str(air_cooler_start)}', font_size=24)
        air_cooler_label = Label(text=f'Воздушное охлаждение: {str(air_cooler_start)} - {str(water_cooler_start)}', font_size=24)
        water_cooler_label = Label(text=f'Водяное охлаждение: {str(water_cooler_start)} - {str(pressing_end)}', font_size=24)

        gl = GridLayout(cols=1)
        gl.add_widget(name_label)
        gl.add_widget(heat_label)
        gl.add_widget(pressing_label)
        gl.add_widget(air_cooler_label)
        gl.add_widget(water_cooler_label)
        gl.add_widget(Button(
            text='Назад',
            background_color=[.96, .19, .19, 1],
            size_hint=[None, None],
            size=[70, 30],
            on_press=window.dismiss
        ))

        window.add_widget(gl)

        window.open()


class ScheduleModesScreenManual(Screen):
    inp_heat = ObjectProperty()
    inp_pressing = ObjectProperty()
    inp_air = ObjectProperty()
    inp_water = ObjectProperty()
    hour_input = ObjectProperty()
    minute_input = ObjectProperty()

    def get_manual_mode(self):
        window = ModalView(auto_dismiss=False)

        try:
            time = dt.timedelta(hours=int(self.hour_input.text), minutes=int(self.minute_input.text))
            heat = dt.timedelta(minutes=int(self.inp_heat.text))
            pressing = dt.timedelta(minutes=int(self.inp_pressing.text))
            air = dt.timedelta(minutes=int(self.inp_air.text))
            water = dt.timedelta(minutes=int(self.inp_water.text))
        except:
            time = dt.timedelta(hours=0, minutes=0)
            heat = dt.timedelta(minutes=0)
            pressing = dt.timedelta(minutes=0)
            air = dt.timedelta(minutes=0)
            water = dt.timedelta(minutes=0)

        heat_start = time

        time += heat
        pressing_start = time

        time += pressing
        air_cooler_start = time

        time += air
        water_cooler_start = time

        time += water
        pressing_end = time

    
        heat_label = Label(text=f'Прогрев: {str(heat_start)} - {str(pressing_start)}', font_size=24)
        pressing_label = Label(text=f'Прессование: {str(pressing_start)} - {str(air_cooler_start)}', font_size=24)
        air_cooler_label = Label(text=f'Воздушное охлаждение: {str(air_cooler_start)} - {str(water_cooler_start)}', font_size=24)
        water_cooler_label = Label(text=f'Водяное охлаждение: {str(water_cooler_start)} - {str(pressing_end)}', font_size=24)

        gl = GridLayout(cols=1)
        gl.add_widget(heat_label)
        gl.add_widget(pressing_label)
        gl.add_widget(air_cooler_label)
        gl.add_widget(water_cooler_label)
        gl.add_widget(Button(
            text='Назад',
            background_color=[.96, .19, .19, 1],
            size_hint=[None, None],
            size=[70, 30],
            on_press=window.dismiss
        ))

        window.add_widget(gl)
        window.open()



kv=Builder.load_file('Press.kv')


class PressApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ScheduleModesScreen(name='modes'))
        sm.add_widget(ScheduleModesScreenManual(name='manual_modes'))
        return sm


if __name__ == '__main__':
    PressApp().run()
