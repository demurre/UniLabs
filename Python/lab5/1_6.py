from kivy.app import App
from kivy.uix.image import Image

class MainApp(App):
    def build(self):
        img = Image(
            source='D:/test-data/thumbnail.png',
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.2, 'center_y': 0.2}
        )
        return img

if __name__ == '__main__':
    MainApp().run()
