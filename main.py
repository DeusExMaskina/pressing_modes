from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.config import Config
from kivy.properties import ObjectProperty

import datetime as dt
import json


Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'minimum_width', 200)
Config.set('graphics', 'minimum_height', 400)

BTN_COLOR = [.39, .67, .82, 1]
BTN_COLOR_CLOSE = [.96, .19, .19, 1]
BTN_COLOR_CREATE = [.13, .78, 0, 1]


class MainScreen(Screen):
    pass


class ScheduleScreen(Screen):  # <== дописать логику и методы ввода и вывода
    def add_plate(self):
        with open('plate.json', 'r') as file:
            self.data = json.load(file)

        window = ModalView(auto_dismiss=False)
        gl = GridLayout(cols=5)

        for i in self.data:
            gl.add_widget(Button(text=self.data[i]['name'][0]))

        window.add_widget(gl)
        window.open()


class ScheduleModesScreen(Screen):
    time_btn = ObjectProperty()
    hour_input = ObjectProperty()
    minute_input = ObjectProperty()

    def get_time_btn(self, *args):
        with open('plate.json', 'r') as file:
            self.data = json.load(file)

        window = ModalView(auto_dismiss=False)
        gl = GridLayout(cols=3, padding=10)

        gl.add_widget(Button(
            text='Назад',
            background_color=[.96, .19, .19, 1],
            size_hint=[None, None],
            size=[70, 30],
            on_press=window.dismiss
        ))

        for i in self.data:
            gl.add_widget(Button(
                text=i,
                size_hint=[None, None],
                size=[70, 30],
                on_press=self.get_modes
            ))

        window.add_widget(gl)
        window.open()

    def get_modes(self, *args):  # <== дописать вывод и логику
        window = ModalView(auto_dismiss=False)
        minute = int(self.minute_input.text)  # <== Добавить блок try
        hour = int(self.hour_input.text)  # <== Добавить блок try
        mark = args[0].text

        with open('plate.json', 'r') as file:
            self.data = json.load(file)

        plate = self.data[mark]
        print(type(plate), plate)

        gl = GridLayout(cols=1)

        window.add_widget(gl)

        window.open()


class PressApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ScheduleScreen(name='schedule'))
        sm.add_widget(ScheduleModesScreen(name='modes'))
        return sm


if __name__ == '__main__':
    PressApp().run()
