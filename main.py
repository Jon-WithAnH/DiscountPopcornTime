from Scrapers.tmbd import TmbdScraper
from Pages.SearchPage import SearchPage
from Pages.LoginPage import LoginPage
from Pages.SeasonsPage import SeasonsPage
from Pages.EpisodesPage import EpisodePage
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.app import App

class DiscountPopcornTime(App):

    def build(self):
        scraper = TmbdScraper()
        sm = ScreenManager(transition=NoTransition())
        # sm.
        # sm.switch_to("")
        Window.size = (1550, 920)
        sm.add_widget(LoginPage(scraper, name='login'))
        sm.add_widget(SearchPage(scraper, name='search'))
        sm.add_widget(SeasonsPage(scraper, name='seasons'))
        sm.add_widget(EpisodePage(scraper, name='episodes'))
        return sm
 
 
if __name__ == "__main__":
   DiscountPopcornTime().run()