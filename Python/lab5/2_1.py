from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


class FirstKivy(App):

    def txt_callback(self, instance, value):
        self.label1.text = value

    def focus_callback(self, instance, value):
        if value:
            self.label2.text = "Field chosen"
        else:
            self.label2.text = "Text field not chosen"

    def build(self):
        self.layout = FloatLayout()

        self.txt_in = TextInput(
            hint_text='Enter text',
            size_hint=(.4, .1),
            pos=(250, 250)
        )

        self.label1 = Label(
            text="Start typing...",
            pos=(15, 75),
            font_size=25
        )

        self.label2 = Label(
            text="Focus state",
            pos=(15, -75),
            font_size=25
        )

        self.txt_in.bind(text=self.txt_callback)
        self.txt_in.bind(focus=self.focus_callback)

        self.layout.add_widget(self.txt_in)
        self.layout.add_widget(self.label1)
        self.layout.add_widget(self.label2)

        return self.layout


if __name__ == '__main__':
    FirstKivy().run()
