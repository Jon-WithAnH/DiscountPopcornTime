from Scrapers.tmbd import TmbdScraper
from Pages.ExtendedFunctions import WrappedLabel, CustomButton, DBButton, SubmitButton

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage

from kivy.clock import mainthread
import threading

class LoginPage(Screen):
    """Inital landing page for the app"""
    def __init__(self, scraper: TmbdScraper, **kw):
        super().__init__(**kw)
        self.tmdb_parser = scraper

        # Loader.num_workers = 20
        self.next_button = Button()
        parent = GridLayout(rows=2)
        self.popular_page_parent = GridLayout(cols=5, rows=4)

        self.popular_page_data =  GridLayout(cols=1,rows=1)
        self.popular_page_data.add_widget(Label(text="Loading popular content from TMDB.\nPlease wait..."))

        self.popular_page_parent.add_widget(self.popular_page_data)
        parent.add_widget(self.build_search_layout())
        parent.add_widget(self.popular_page_parent)
        # self.manager = "search"
        thread = threading.Thread(target=self.getPopularData)
        thread.daemon = True
        thread.start()
        self.add_widget(parent)

    def build_search_layout(self):
        search_layout = GridLayout(cols=4,size_hint_y=None, height=30)
        back_button = Button(text="<-", size_hint_x=None, width=20, disabled=True)
        self.next_button = Button(text="->", size_hint_x=None, width=20, disabled=True, on_press=self.change)
        search_bar = TextInput(multiline=False, _hint_text="Enter a search", height=30,  size_hint_y=None, on_text_validate=self.submit_query)
        serach_button = Button(text="Search", size_hint=[None, None], height=30, on_press=self.change)
        search_layout.add_widget(back_button)
        search_layout.add_widget(self.next_button)
        search_layout.add_widget(search_bar)
        search_layout.add_widget(serach_button)
        return search_layout
    
    def submit_query(self, input: TextInput):
        if not input.text:
            print("Nothing submitted")
            return
        # print(f"query submitted for {input.text}")
        test1 = self.manager.get_screen("search")
        test1.preform_search(input)
        self.manager.current = 'search'
        # global_query = input.text
        

    def buildFromPopularPage(self, data: dict):
        # assert len(data)==4*5
        parent = GridLayout(cols=5, rows=4)
        for each in range(len(data)):
            level_2 = BoxLayout(orientation='horizontal', spacing=10)
            thumby = data[each][-2]
            float_test = FloatLayout()
            if thumby == "":
                level_2.add_widget(float_test.add_widget(WrappedLabel(text="No Image", pos_hint={"center_x": .5, "center_y": .5})))
            else:
                float_test.add_widget(AsyncImage(source=thumby, pos_hint={"center_x": .5, "center_y": .5}))
                level_2.add_widget(float_test)

            float_test.add_widget(DBButton("FAV", data[each], pos_hint={"center_x": .1, "center_y": .9}))
            float_test.add_widget(DBButton('WL', data[each], pos_hint={"center_x": .9, "center_y": .9}))
            level_3 = GridLayout(rows=4)
            level_3.add_widget(WrappedLabel(text=data[each][0]))
            level_3.add_widget(WrappedLabel(text=data[each][1]))
            level_3.add_widget(WrappedLabel(text=data[each][2]))
            level_3.add_widget(SubmitButton(data[each][-1], text='Select', background_normal=""))
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        return parent  

    def getPopularData(self):
        tmp = self.tmdb_parser.get_popular_movies()
        self.setData(tmp)

    @mainthread
    def setData(self, data: dict):
        self.popular_page_parent.clear_widgets()
        self.popular_page_parent.add_widget(self.buildFromPopularPage(data))
        
        # self.popular_page_data

    def change(self, button: Button):
        """Used to transition the screen upon a search request

        Args:
            button (Button): Required peremeter for the button used to trigger this function
        """
        self.manager.current="search"