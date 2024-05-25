from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import requests
from config import API_KEY, API_URL


class WeatherCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def weather_search(self):
        city = self.ids.city_field.text.strip().lower() #отримуємо з стайл кв назву міста
        api_params = {
            'q': city,
            'appid': API_KEY
        }
        data = requests.get(API_URL, api_params)# запит до сервісу погоди з параметрами
        response = data.json()#отримуємо в-дь у форматі json
        print(response)
        description = response["weather"][0]["description"]
        self.ids.weather_card.ids.label.text = description

class MainApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.screen = MainScreen("main_screen")
        return self.screen


MainApp().run()