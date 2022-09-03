from Scrapers.tmbd import TmbdScraper

from Pages.SearchPage import SearchPage
from Pages.LoginPage import LoginPage
from Pages.SeasonsPage import SeasonsPage
from Pages.EpisodesPage import EpisodePage
from Pages.DBReleatedPage import DBRelatedPage
from Pages.SearchLayout import SearchLayout
from Pages.ResultsLayout import ResultsLayout
from Pages.PageNumbers import PageNumbers
import Pages.ExtendedFunctions

from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.core.window import Window
from kivy.app import App
from kivy.loader import Loader
from kivy.lang import Builder

from os import listdir
from sys import argv

class DiscountPopcornTime(App):
    kv_directory = 'Pages'
    def build(self):
        scraper = TmbdScraper()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(LoginPage(scraper, name='login'))
        sm.add_widget(SearchPage(scraper, name='search'))
        sm.add_widget(SeasonsPage(scraper, name='seasons'))
        sm.add_widget(EpisodePage(scraper, name='episodes'))
        sm.add_widget(DBRelatedPage(scraper, name='dblist'))

        return sm
 
 
if __name__ == "__main__":
    Loader.num_workers = 20 # Maximize thread usage to load all images as fast as possible
    Window.size = (1550, 920)
    if len(argv) > 1:
        # Enable internet brower usage
        supported_browser_alias = ['/b', '/browser']
        for each in supported_browser_alias:
            if each in argv:
                print("Browser use is active")
                Pages.ExtendedFunctions.ENABLE_BROWSER_USE = True
            
    # Window.custom_titlebar = True
    kv_path = "./kv_files/"
    for kv in listdir(kv_path):
        Builder.load_file(kv_path+kv)
    # Window.set_title("TT")
    DiscountPopcornTime().run()
