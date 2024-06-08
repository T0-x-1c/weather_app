from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import requests
from config import API_KEY, API_URL, FORECAST_URL
import json

with open('setting.json', 'r', encoding='utf-8') as file:
    setting = json.load(file)

def save():
    with open('setting.json', 'w', encoding='utf-8') as file:
        json.dump(setting, file, ensure_ascii=False, sort_keys=True, indent=4)


class WeatherCard(MDCard):
    def __init__(self, description, icon, humidity, temp, rain, wind, feel_like, city_name, date_time, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.feels_like_text.text = f"Відчувається як {feel_like}°C"
        self.ids.humidity_text.text = f"Вологість: {humidity}%"
        self.ids.rain_text.text = f"Опади: {rain}%"
        self.ids.wind_text.text = f"Вітер: {wind} км/год"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        self.ids.city_name_text.text = f"{city_name}"
        self.ids.date_time.text = f"{date_time}"

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_weather_data(self, url, city):
        api_params = {
            'q': city,
            'appid': API_KEY
        }

        data = requests.get(url, api_params)  # запит до сервісу погоди з параметрами
        response = data.json()  # отримуємо в-дь у форматі json
        return response

    def add_weather_card(self, response):
        # try:
        description = response['weather'][0]["description"]
        icon = response['weather'][0]["icon"]
        humidity = response['main']["humidity"]
        temp = response['main']["temp"]
        feel_like = response['main']["feels_like"]
        if 'rain' in response:
            if '1h' in response['rain']:
                rain = response['rain']["1h"]
            else:
                rain = response['rain']["3h"]
        else:
            rain = 0
        wind = response["wind"]["speed"]
        if "name" in response:
            city_name = response["name"]
        else:
            city_name = self.city

        if "dt_txt" in response:
            date_time = response['dt_txt'][5:-3]
        else:
            date_time = "Зараз"


        new_card = WeatherCard(description, icon, humidity, temp, rain, wind, feel_like, city_name, date_time)
        self.ids.weather_carousel.add_widget(new_card)
        # setting["last_search"] = city_name
        # save()

        # except:
        #     print("такого міста немає")
    def weather_search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_field.text.strip().lower() #отримуємо з стайл кв назву міста
        self.city = city

        current_weather = self.get_weather_data(API_URL, city)
        forecast = self.get_weather_data(FORECAST_URL, city)
        if current_weather:
            self.add_weather_card(current_weather)
        if forecast:
            for period in forecast['list']:
                self.add_weather_card(period)

class MainApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.screen = MainScreen("main_screen")
        return self.screen

MainApp().run()