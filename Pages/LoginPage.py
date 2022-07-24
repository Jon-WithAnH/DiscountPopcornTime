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
from kivy.uix.dropdown import DropDown

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

    def work_in_progress(self, button: Button):
        parent = FloatLayout()
        dropdown = DropDown(size_hint=[.1,1], pos=(0,-30))
        options = ["Home", "Favorites", "Watch Later", "History"]
        for each in options:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            btn = Button(text='%s' % each, size_hint_y=None, height=44, on_press=self.switch)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            # then add the button inside the dropdown
            dropdown.add_widget(btn)

        parent.add_widget(dropdown)
        self.add_widget(parent)

    def build_search_layout(self):
        search_layout = GridLayout(cols=5,size_hint_y=None, height=30)
        dropdown = Button(text="...", size_hint_x=None, width=20, on_press=self.work_in_progress)
        back_button = Button(text="<-", size_hint_x=None, width=20, disabled=True)
        self.next_button = Button(text="->", size_hint_x=None, width=20, disabled=True, on_press=self.change)
        search_bar = TextInput(multiline=False, _hint_text="Enter a search", height=30,  size_hint_y=None, on_text_validate=self.submit_query)
        serach_button = Button(text="Search", size_hint=[None, None], height=30, on_press=self.change)
        search_layout.add_widget(dropdown)
        search_layout.add_widget(back_button)
        search_layout.add_widget(self.next_button)
        search_layout.add_widget(search_bar)
        search_layout.add_widget(serach_button)
        return search_layout
    
    def switch(self, button):
        self.manager.current = 'dblist'

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
                thumby = 'https://www.themoviedb.org' + thumby
                float_test.add_widget(AsyncImage(source=thumby, pos_hint={"center_x": .5, "center_y": .5}))
                level_2.add_widget(float_test)

            float_test.add_widget(DBButton("FAV", data[each], pos_hint={"center_x": .1, "center_y": .9}))
            float_test.add_widget(DBButton('WL', data[each], pos_hint={"center_x": .9, "center_y": .9}))
            level_3 = GridLayout(rows=4)
            level_3.add_widget(WrappedLabel(text=data[each][0]))
            level_3.add_widget(WrappedLabel(text=data[each][1]))
            level_3.add_widget(WrappedLabel(text=data[each][2]))
            level_3.add_widget(SubmitButton(data[each][-1], text='Select', background_normal="Pages\\resources\\transparent.png"))
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