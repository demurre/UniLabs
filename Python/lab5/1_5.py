from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class FirstKivy(App):
    def build(self):
        self.lay = BoxLayout(
            orientation='horizontal',
            padding=25,
            spacing=10
        )

        self.button1 = Button(text="Button 1")
        self.button2 = Button(text="Button 2")

        self.lay.add_widget(self.button1)
        self.lay.add_widget(self.button2)

        return self.lay


if __name__ == "__main__":
    FirstKivy().run()
