from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import requests
from config import API_KEY, API_URL


class WeatherCard(MDCard):
    def __init__(self, description, icon, humidity, temp, rain, wind, feel_like, city_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.feels_like_text.text = f"Відчувається як {feel_like}°C"
        self.ids.humidity_text.text = f"Вологість: {humidity}%"
        self.ids.rain_text.text = f"Опади: {rain}%"
        self.ids.wind_text.text = f"Вітер: {wind} км/год"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        print(city_name)
        self.ids.city_name_text.text = f"{city_name}"

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def weather_search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_field.text.strip().lower() #отримуємо з стайл кв назву міста
        api_params = {
            'q': city,
            'appid': API_KEY
        }
        data = requests.get(API_URL, api_params)# запит до сервісу погоди з параметрами
        response = data.json()#отримуємо в-дь у форматі json
        print(response)
        description = response['weather'][0]["description"]
        icon = response['weather'][0]["icon"]
        humidity = response['main']["humidity"]
        temp = response['main']["temp"]
        feel_like = response['main']["feels_like"]
        if 'rain' in response:
            rain = response['rain']["1h"]
        else:
            rain = 0
        wind = response["wind"]["speed"]
        city_name = response["name"]
        print(city_name)

        new_card = WeatherCard(description, icon, humidity, temp, rain, wind, feel_like, city_name)
        self.ids.weather_carousel.add_widget(new_card)

class MainApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.screen = MainScreen("main_screen")
        return self.screen


MainApp().run()