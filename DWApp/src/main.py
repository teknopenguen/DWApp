from kivy.app import App
from kivymd.theming import ThemeManager
from sm import SM


class DWApp(App):
    theme_cls = ThemeManager(theme_style='Light')

    def build(self):
        return SM()


if __name__ == '__main__':

    DWApp().run()
