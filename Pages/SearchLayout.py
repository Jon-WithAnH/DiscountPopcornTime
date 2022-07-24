from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

from Pages.ResultsLayout import ResultsLayout

class SearchLayout(Screen):
    search_bar = ObjectProperty()
    manager = ObjectProperty()  # Required to intereact with the ScreenManager
    
    def __init__(self, **kw):
        super().__init__(**kw)

    def preform_search(self):
        if self.search_bar.text == "":
            print("No query")
            return
        self.manager.get_screen("search").preform_search(self.search_bar)
        self.manager.current = 'search'

    def debug(self):
        print(self.manager.current)

    def gen_dropdown(self):
        parent = FloatLayout()
        dropdown = DropDown(size_hint=[.1,1], pos=(0,-30))
        options = ["Home", "Favorites", "Watch Later", "Watch History"]
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
        # We want to superceed the widgets placed in whichever layout is beneath SearchLayout
        # We can add the widget directly to Window to achieve this
        Window.add_widget(parent)

    def switch(self, button):
        if button.text == "Home":
            self.manager.current = 'login'
            return
        self.manager.current = 'dblist'
        # print((button.text.lower()).replace(" ", "_"))
        ResultsLayout.desired_page = (button.text.lower()).replace(" ", "_")
        test = self.manager.get_screen("dblist")
        test.preform_search()
