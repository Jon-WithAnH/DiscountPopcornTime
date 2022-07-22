from Scrapers.tmbd import TmbdScraper

from Pages.SearchPage import SearchPage
from Pages.LoginPage import LoginPage
from Pages.SeasonsPage import SeasonsPage
from Pages.EpisodesPage import EpisodePage

from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.app import App
from kivy.loader import Loader

class DiscountPopcornTime(App):

    def build(self):
        scraper = TmbdScraper()
        sm = ScreenManager(transition=NoTransition())
        # sm.
        # sm.switch_to("")
        sm.add_widget(LoginPage(scraper, name='login'))
        sm.add_widget(SearchPage(scraper, name='search'))
        sm.add_widget(SeasonsPage(scraper, name='seasons'))
        sm.add_widget(EpisodePage(scraper, name='episodes'))
        return sm
 
 
if __name__ == "__main__":
    Loader.num_workers = 20 # Maximize thread usage to load all images as fast as possible
    Window.size = (1550, 920)
    DiscountPopcornTime().run()