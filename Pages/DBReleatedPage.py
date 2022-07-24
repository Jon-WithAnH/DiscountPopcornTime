"""Page used to access database. Display's lists such as favorites, watch later, and history"""

from tkinter import Button, Label
from turtle import Screen
from Scrapers.tmbd import TmbdScraper
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class DBRelatedPage(Screen):
    # pass
    rlayout = ObjectProperty()
    def __init__(self, scraper: TmbdScraper, **kw) -> None:
        super().__init__(**kw)
        # test = GridLayout(cols=2)
        # test.add_widget(Label(text="TT"))
        # self.add_widget(test)
    
    # def build(self):
    #     return Button(text="meh")
    def preform_search(self):
        # print("Hello")
        # print(self.get_root_window())
        self.rlayout.gen_favorites()


    