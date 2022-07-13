from kivy.uix.button import Button
from kivy.uix.label import Label

class CustomButton(Button):

    def __init__(self, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link
    
    def on_press(self):
        print(self.link)

class WrappedLabel(Label):
    # Based on Tshirtman's answer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))