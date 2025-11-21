from kivy.app import App
from kivy.uix.textinput import TextInput

class FirstKivy(App):
    def build(self):
        return TextInput(
            hint_text='Enter text',
            size_hint=(0.1, 0.1),
            pos=(200, 200)
        )

if __name__ == '__main__':
    FirstKivy().run()
