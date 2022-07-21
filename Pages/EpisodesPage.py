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

class EpisodePage(Screen):
        
        def __init__(self, tmbdScraper: TmbdScraper, **kw):
            super().__init__(**kw)
            self.tmbd_parser = tmbdScraper

        
        def get_episodes_info(self, button: CustomButton):
            # print(f"From EpisodesPage: {button.link}")
            data = self.tmbd_parser.get_episodes(button.link)
            print(f"Found {len(data)} episodes")
            self.build_episodes_page(data)

        def build_episodes_page(self, data: dict):
            scroll = ScrollView()
            scroll.scroll_wheel_distance=100
            tmp = 220*int((len(data)/2+1))/Window.height
            parent = GridLayout(cols=2, rows=int(len(data)/2)+1, size_hint_y = tmp)

            for each in data:
                level_2 = BoxLayout(orientation='horizontal', spacing=10, size_hint_y = None, height=220)
                if not data[each][-2].__contains__('svg'):
                    thumby = 'https://www.themoviedb.org' + data[each][-2]
                    level_2.add_widget(AsyncImage(source=thumby))
                else:
                    level_2.add_widget(Label(text="No Image"))
                level_3 = GridLayout(rows=4)
                level_3.add_widget(WrappedLabel(text=data[each][1]))
                level_3.add_widget(WrappedLabel(text=data[each][2]))
                level_3.add_widget(WrappedLabel(text=data[each][4]))
                level_3.add_widget(CustomButton(data[each][-1], text='Select', on_press=self.select_episode))
                level_2.add_widget(level_3)
                parent.add_widget(level_2)
            scroll.add_widget(parent)
            self.clear_widgets()
            self.add_widget(scroll)           
        
        def select_episode(self, button: CustomButton):
            # /tv/14658-survivor/season/42/episode/1
            info = button.link.split("/")
            ep_num = info[-1]
            season_num = info[-3]
            tmdb_num = info[2] # 14658-survivor
            tmdb_num = tmdb_num.split("-")[0]
            # URL: https://fsapi.xyz/tv-tmdb/{TMDb_ID}-{SEASON_NUMBER}-{EPISODE_NUMBER}
            print(f"https://fsapi.xyz/tv-tmdb/{tmdb_num}-{season_num}-{ep_num}")