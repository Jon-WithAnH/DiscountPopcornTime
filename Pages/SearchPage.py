from Scrapers.tmbd import TmbdScraper
from Pages.ExtendedFunctions import WrappedLabel, CustomButton, DBButton

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.clock import mainthread

# from Scrapers.tmbd import TmbdScraper
# import Scrapers.tmbd
# from Scrapers.tmbd.py import TmbdScraper

class SearchPage(Screen):

    def test(self):
        print("Hello from test!")

    def __init__(self, tmbdScraper: TmbdScraper, **kw):
        super().__init__(**kw)
        self.tmbd_parser = tmbdScraper

        parent = GridLayout(rows=2)
        self.popular_page_parent = GridLayout(cols=5, rows=4)

        self.popular_page_data =  GridLayout(cols=1,rows=1)
        self.popular_page_data.add_widget(Label(text="Loading your query from TMDB.\nPlease wait..."))

        self.popular_page_parent.add_widget(self.popular_page_data)
        parent.add_widget(self.build_search_layout())
        parent.add_widget(self.popular_page_parent)
        # self.manager = "search"
        self.add_widget(parent)

    def change(self, button):
        # button.text="It changed"
        self.manager.current="login"
        
    def build_search_layout(self):
        search_layout = GridLayout(cols=4,size_hint_y=None, height=30)
        back_button = Button(text="<-", size_hint_x=None, width=20, on_press=self.go_back_button)
        next_button = Button(text="->", size_hint_x=None, width=20, disabled=True)
        search_bar = TextInput(multiline=False, _hint_text="Enter a search", height=30,  size_hint_y=None, on_text_validate=self.preform_search)
        serach_button = Button(text="Search", size_hint=[None, None], height=30, on_press=self.change)
        search_layout.add_widget(back_button)
        search_layout.add_widget(next_button)
        search_layout.add_widget(search_bar)
        search_layout.add_widget(serach_button)
        return search_layout

    def go_back_button(self, button):
        test1 = self.manager.get_screen("login")
        test1.next_button.disabled = False
        self.manager.current = 'login'

    def preform_search(self, query: str):
        """Method is activated when user sends a search request. It is called within LoginPage.submitQuery(). Page should be inaccessable until this method is actiaved.

        Args:
            query (str): Desired search term for TMDB
        """
        tmp = self.tmbd_parser.preform_search_query(query.text)
        if tmp is None:
            print("movie")
            return
        print(f"Search completed for {query.text}: {len(tmp)} results")
        self.buildFromSearchPage(tmp)
        # self.setData(tmp)

    @mainthread
    def buildFromSearchPage(self, data: dict):
        # assert len(data)==4*5
        # print(data[0])
        # exit(0)
        if len(data) == 0:
            self.popular_page_parent.clear_widgets()
            self.popular_page_parent.add_widget(Label(text="No results found"))
            return

        parent = GridLayout(cols=5, rows=4)
        for each in range(len(data)):
            level_2 = BoxLayout(orientation='horizontal', spacing=10)
            float_test = FloatLayout()
            if not data[each][3] == "":
                # Reaplacing the size of the images to match the images from the front page
                # https://www.themoviedb.org/t/p/w94_and_h141_bestv2/5R125JAIh1N38pzHp2dRsBpOVNY.jpg
                # https://www.themoviedb.org/t/p/w220_and_h330_face/9HFFwZOTBB7IPFmn9E0MXdWave3.jpg
                data[each][3] = data[each][3].replace("94", "220")
                data[each][3] = data[each][3].replace("141", "330")
                thumby = 'https://www.themoviedb.org' + data[each][3]  
                float_test.add_widget(AsyncImage(source=thumby, pos_hint={"center_x": .5, "center_y": .5}))
                level_2.add_widget(float_test)
            else:
                float_test.add_widget(Image(source="Pages\\resources\\noimageBlack.png", pos_hint={"center_x": .5, "center_y": .5}))
                level_2.add_widget(float_test)
            float_test.add_widget(DBButton("FAV", data[each], pos_hint={"center_x": .1, "center_y": .9}))
            float_test.add_widget(DBButton('WL', data[each], pos_hint={"center_x": .9, "center_y": .9}))
            level_3 = GridLayout(rows=4)
            # level_3.add_widget(WrappedLabel(text=data[each][0], color=[125,125,125,1]))
            level_3.add_widget(WrappedLabel(text=data[each][0]))
            level_3.add_widget(WrappedLabel(text=data[each][1]))
            level_3.add_widget(WrappedLabel(text=data[each][2]))
            level_3.add_widget(CustomButton(data[each][4], text='Select', on_press=self.selected_content))
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        self.popular_page_parent.clear_widgets()
        self.popular_page_parent.add_widget(parent)
        return parent  

    def selected_content(self, button:CustomButton):
        # print(f'https://www.themoviedb.org{button.link}')
        test1 = self.manager.get_screen("seasons")
        result = test1.get_seasons_info(button)
        print(result)
        if result:
            self.manager.current = 'seasons'        
        # self.manager.switch_to('login', direction='left')