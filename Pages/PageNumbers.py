"""Footer that provide multiple page functionality of layouts"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class PageNumbers(Screen):
    manager = ObjectProperty()  # Required to intereact with the ScreenManager

    def update(self):
        test = self.manager.get_screen("dblist")
        test.preform_search()