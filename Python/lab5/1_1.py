from kivy.app import App
from kivy.uix.label import Label

class FirstKivy(App):
    def build(self):
        return Label(
            text='[color=FF0000][b]Yarik[/b][/color]',
            markup=True,
            font_size=10,
            pos=(-400, 400)
        )

if __name__ == '__main__':
    FirstKivy().run()
