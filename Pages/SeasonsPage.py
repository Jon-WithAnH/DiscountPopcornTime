from Scrapers.tmbd import TmbdScraper
from Pages.ExtendedFunctions import WrappedLabel, CustomButton

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
# from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.clock import mainthread
from kivy.uix.scrollview import ScrollView

class SeasonsPage(Screen):
    
    def __init__(self, tmbdScraper: TmbdScraper, **kw):
        super().__init__(**kw)
        self.tmbd_parser = TmbdScraper()

    def get_seasons_info(self, button: CustomButton) -> bool:
        """Feeds the parser link information contained within the button.

        Args:
            button (CustomButton): CustomButton that holds the link to wherever the user wants to go. Eg., "/movie/19995"

        Returns:
            bool: False if it is a movie or an anime. True if it's a TV show and the parser pulled relevent data.
        """
        # print(f"From SeasonsPage: {button.link}")
        season_info = self.tmbd_parser.get_season(button.link)
        if season_info is None:
            tmp = button.link.split("/")
            print(f"https://www.themoviedb.org{button.link}")
            print(f"https://fsapi.xyz/tmdb-movie/{tmp[-1]}")
            # https://fsapi.xyz/tmdb-movie/19995
            return False
        print(f"Found {len(season_info)} seasons")
        self.build_seasons_page(season_info)
        return True

    def build_seasons_page(self, data: dict):
        scroll = ScrollView()
        scroll.scroll_wheel_distance=100
        test = Window.height / 220
        tmp = 220*int((len(data)/2+1))/Window.height
        # print(f"recommend size_hint_y: {tmp} - resulted from {220}*{int(len(data)/2+1)}/{Window.height}")
        parent = GridLayout(cols=2, rows=int(len(data)/2)+1, size_hint_y = tmp)

        for each in data:
            level_2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y = None, height=220)
            if not data[each][3] == "":
                thumby = 'https://www.themoviedb.org' + data[each][3]
                level_2.add_widget(AsyncImage(source=thumby))
            else:
                level_2.add_widget(Label(text="No Image"))
            level_3 = GridLayout(rows=4)
            level_3.add_widget(WrappedLabel(text=data[each][0]))
            level_3.add_widget(WrappedLabel(text=data[each][1]))
            level_3.add_widget(WrappedLabel(text=data[each][2]))
            level_3.add_widget(CustomButton(data[each][4], text='Select', on_press=self.select_season))
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        scroll.add_widget(parent)
        self.clear_widgets()
        self.add_widget(scroll)

    def select_season(self, button: CustomButton):
        # print(f'https://www.themoviedb.org{button.link}')
        test1 = self.manager.get_screen("episodes")
        test1.get_episodes_info(button)
        self.manager.current = 'episodes'  