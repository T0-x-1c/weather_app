from kivymd.app import MDApp as App
from kivymd.uix.label import MDLabel as Label


class MainApp(App):
    def build(self):
        return Label(text="Hello, World", halign="center")


MainApp().run()