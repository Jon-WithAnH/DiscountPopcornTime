'''Placeholder'''

from cgitb import text
from os import TMP_MAX
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
# from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.clock import mainthread

from Scrapers.tmbd import TmbdScraper
from Pages.SearchPage import SearchPage as sp

import threading

class CustomButton(Button):

    def __init__(self, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link
    
    def on_press(self):
        print(self.link)

class WrappedLabel(Label):
    # Based on Tshirtman's answer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

global_query = ""

class LoginPage(Screen):
    """Inital landing page for the app"""
    def __init__(self, **kw):
        super().__init__(**kw)
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
        print(f"query submitted for {input.text}")
        test1 = self.manager.get_screen("search")
        test1.preform_search(input.text)
        self.manager.current = 'search'
        print(f"test: {test1}")
        global_query = input.text
        

    def buildFromPopularPage(self, data: dict):
        # assert len(data)==4*5
        parent = GridLayout(cols=5, rows=4)
        for each in range(len(data)):
            level_2 = BoxLayout(orientation='horizontal', spacing=10)
            thumby = data[each][4]
            level_2.add_widget(AsyncImage(source=thumby))
            level_3 = GridLayout(rows=4)
            # level_3.add_widget(WrappedLabel(text=data[each][0], color=[125,125,125,1]))
            level_3.add_widget(WrappedLabel(text=data[each][0]))
            level_3.add_widget(WrappedLabel(text=data[each][1]))
            level_3.add_widget(WrappedLabel(text=data[each][2]))
            level_3.add_widget(CustomButton(data[each][3], text='Select'))
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        return parent  

    def getPopularData(self):
        tmp = TmbdScraper()
        tmp = tmp.get_popular_movies()
        self.setData(tmp)

    @mainthread
    def setData(self, data: dict):
        self.popular_page_parent.clear_widgets()
        self.popular_page_parent.add_widget(self.buildFromPopularPage(data))
        
        # self.popular_page_data

    def change(self, button):
        # button.text="It changed"
        # self.getPopularData()
        self.manager.current="search"
        # self.root.prolly_wont_work()


class SearchPage(Screen):

    def test(self):
        print("Hello from test!")

    def __init__(self, **kw):
        super().__init__(**kw)

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
        tmp = TmbdScraper()
        tmp = tmp.preform_search_query(query.text)
        print(f"search completed for {query.text}: {len(tmp)} results")
        self.buildFromSearchPage(tmp)
        # self.setData(tmp)

    @mainthread
    def buildFromSearchPage(self, data: dict):
        # assert len(data)==4*5
        # print(data[0])
        # exit(0)
        parent = GridLayout(cols=5, rows=4)
        for each in range(len(data)):
            level_2 = BoxLayout(orientation='horizontal', spacing=10)
            if not data[each][3] == "":
                thumby = 'https://www.themoviedb.org' + data[each][3]
                level_2.add_widget(AsyncImage(source=thumby))
            else:
                level_2.add_widget(Label(text="No Image"))
            level_3 = GridLayout(rows=4)
            # level_3.add_widget(WrappedLabel(text=data[each][0], color=[125,125,125,1]))
            level_3.add_widget(WrappedLabel(text=data[each][0]))
            level_3.add_widget(WrappedLabel(text=data[each][1]))
            level_3.add_widget(WrappedLabel(text=data[each][2]))
            level_3.add_widget(CustomButton('https://www.themoviedb.org' + data[each][4], text='Select'))
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        self.popular_page_parent.clear_widgets()
        self.popular_page_parent.add_widget(parent)
        return parent  

        # self.manager.switch_to('login', direction='left')

    # def build(self):
        # return Button(ext="fk")


class Controller:
    pass

class DiscountPopcornTime(App):

    def prolly_wont_work(self):
        print("I guess it did work")

    def build(self):

        sm = ScreenManager(transition=NoTransition())
        # sm.
        # sm.switch_to("")
        Window.size = (1550, 920)
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(SearchPage(name='search'))

        return sm
 
 
if __name__ == "__main__":
   DiscountPopcornTime().run()
