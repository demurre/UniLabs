from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class FirstKivy(App):
    def build(self):
        dropdown = DropDown()

        for index in range(10):
            btn = Button(
                text=f'Element №{index + 1}',
                size_hint_y=None,
                height=20
            )
            dropdown.add_widget(btn)

        mainbutton = Button(
            text='Open',
            size_hint=(None, None),
        )

        mainbutton.bind(on_release=dropdown.open)

        return mainbutton


if __name__ == '__main__':
    FirstKivy().run()
