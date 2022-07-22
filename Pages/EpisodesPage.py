from Scrapers.tmbd import TmbdScraper
from Pages.ExtendedFunctions import SubmitButton, WrappedLabel, CustomButton

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
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
                level_3.add_widget(SubmitButton(data[each][-1], text='Select'))
                level_2.add_widget(level_3)
                parent.add_widget(level_2)
            scroll.add_widget(parent)
            self.clear_widgets()
            self.add_widget(scroll)           
        