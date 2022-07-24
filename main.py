from Scrapers.tmbd import TmbdScraper

from Pages.SearchPage import SearchPage
from Pages.LoginPage import LoginPage
from Pages.SeasonsPage import SeasonsPage
from Pages.EpisodesPage import EpisodePage
from Pages.DBReleatedPage import DBRelatedPage
from Pages.SearchLayout import SearchLayout
from Pages.ResultsLayout import ResultsLayout
# from Pages import *
from Pages.PageNumbers import PageNumbers

from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.core.window import Window
from kivy.app import App
from kivy.loader import Loader
from kivy.lang import Builder

from os import listdir


class DiscountPopcornTime(App):
    kv_directory = 'Pages'
    def build(self):
        scraper = TmbdScraper()
        sm = ScreenManager(transition=NoTransition())
        # sm.
        # sm.switch_to("")
        sm.add_widget(LoginPage(scraper, name='login'))
        sm.add_widget(SearchPage(scraper, name='search'))
        sm.add_widget(SeasonsPage(scraper, name='seasons'))
        sm.add_widget(EpisodePage(scraper, name='episodes'))
        sm.add_widget(DBRelatedPage(scraper, name='dblist'))
        # sm.add_widget(SearchLayout(name='wwww'))
        return sm
 
 
if __name__ == "__main__":
    Loader.num_workers = 20 # Maximize thread usage to load all images as fast as possible
    Window.size = (1550, 920)
    # Window.custom_titlebar = True
    kv_path = "./kv_files/"
    for kv in listdir(kv_path):
        Builder.load_file(kv_path+kv)
    # Window.set_title("TT")
    DiscountPopcornTime().run()