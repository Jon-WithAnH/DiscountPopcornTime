from doctest import UnexpectedException
from kivy.uix.button import Button
from kivy.uix.label import Label
from sql.SqlManager import SqlContextManager

class CustomButton(Button):

    def __init__(self, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link
    
    def on_press(self):
        print(self.link)

class DBButton(Button):

    def __init__(self, data: list, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        # We can infer which DB the button is connected to based on the saved text within the button.
        # To do that, we'll check to make sure the buttons have a text that's supported.
        # Raise an exception if the button's text doesn't match anything supported.

        for i, each in enumerate(SqlContextManager.SUPPORTED_DB_TABLES_ALIAS):
            if self.text == each:
                self.DB = SqlContextManager.SUPPORTED_DB_TABLES[i]

        with SqlContextManager() as manager:
            if manager.search_table(self.DB, self.data):
                self.background_normal = 'Pages\\resources\\newbookmark.png'
            else: self.background_normal = 'Pages\\resources\\emptybookmark.png'

        # raise AttributeError(f"Invalid attritube on DBButton. Unable to parse: \"{self.text}\"")
    
    def on_press(self):
        # print(f"Data to be saved: {self.data}")
        with SqlContextManager() as manager:
            if manager.search_table(self.DB, self.data):
                manager.delete(self.DB, self.data)
                self.background_normal = 'Pages\\resources\\emptybookmark.png'
                return
            manager.commit(self.DB, self.data)
            self.background_normal = 'Pages\\resources\\newbookmark.png'
            

class WrappedLabel(Label):
    # Based on Tshirtman's answer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))