from kivy.app import App
from kivy.uix.button import Button

class MyButton(Button):
    text = "[color=FF0000]Click me![/color]"
    markup = True

    size_hint = (0.1, 0.1)

    pos = (0, 0)

    on_press = lambda self: print("Clicked")

class TutorialApp(App):
    def build(self):
        return MyButton()

if __name__ == "__main__":
    TutorialApp().run()
