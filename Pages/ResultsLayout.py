from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from Pages.ExtendedFunctions import WrappedLabel, CustomButton, DBButton, SubmitButton

from sql.SqlManager import SqlContextManager


class ResultsLayout(Screen):
    manager = ObjectProperty()  # Required to intereact with the ScreenManager
    desired_page = ""

    def get_data(self):
        data = self.manager.get_screen("search").preform_search(TextInput(text='survivor'))
        # self.manager.current = 'search'
        self.buildFromSearchPage(data)

    def buildFromSearchPage(self, data: dict):
        self.clear_widgets()
        # assert len(data)==4*5
        # print(data[0])
        # exit(0)
        # data = self.manager.get_screen("search").preform_search(self.search_bar)
        if len(data) == 0:
            self.add_widget(Label(text="No results found"))
            return

        parent = GridLayout(cols=5, rows=4)
        for each in range(len(data)):
            level_2 = BoxLayout(orientation='horizontal', spacing=10)
            db_layout = FloatLayout()
            if not data[each][3] == "":
                # TODO: Move replace call into the scraper instead of here
                # Replacing the size of the images to match the images from the front page
                # https://www.themoviedb.org/t/p/w94_and_h141_bestv2/5R125JAIh1N38pzHp2dRsBpOVNY.jpg
                # https://www.themoviedb.org/t/p/w220_and_h330_face/9HFFwZOTBB7IPFmn9E0MXdWave3.jpg
                data[each][3] = data[each][3].replace("94", "220")
                data[each][3] = data[each][3].replace("141", "330")
                thumby = 'https://www.themoviedb.org' + data[each][3]  
                db_layout.add_widget(AsyncImage(source=thumby, pos_hint={"center_x": .5, "center_y": .5}))
            else:
                db_layout.add_widget(Image(source="Pages\\resources\\noimageBlack.png", pos_hint={"center_x": .5, "center_y": .5}))
            level_2.add_widget(db_layout)
            db_layout.add_widget(DBButton("FAV", data[each], pos_hint={"center_x": .1, "center_y": .9}))
            db_layout.add_widget(DBButton('WL', data[each], pos_hint={"center_x": .9, "center_y": .9}))
            level_3 = GridLayout(rows=4)
            for i in range(3):
                level_3.add_widget(WrappedLabel(text=data[each][i]))
            level_3.add_widget(self.button_factory(data[each]))
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        self.add_widget(parent)
        return parent  
    
    def button_factory(self, link: list) -> CustomButton | SubmitButton:
        """Takes a list and determines the appropiate button to use based on that the link within the list

        Args:
            link (list): The list belonging to the content in the dict. This will be search at index 4 for /movie/616037 or /tv/14658

        Returns:
            CustomButton | SubmitButton: CustomButtom if the media is a show. SubmitButton if it's a movie
        """
        if link[4].__contains__("movie"):
            return SubmitButton(link[4], text='Select')
        else:
            return CustomButton(link[4], text='Next', on_release=self.preform_search)

    def preform_search(self, button: CustomButton):
        """Works as a go between for the ResultsLayout and SearchPage. IE., manages a transtition
        """
        self.manager.get_screen("seasons").get_seasons_info(button)
        self.manager.current = "seasons"

    def debug(self):
        print(f"Desired: {self.desired_page}")

    def gen_favorites(self):
        print(self.desired_page)
        if self.desired_page == "":
            print("Desired page not set")
            return
        with SqlContextManager() as manager:
            # print(manager.get_all('favorites'))
            data = manager.get_all(self.desired_page)
        data = self.toDict(data)
        self.buildFromSearchPage(data)



    def toDict(self, data: list):
        data_dict = {}
        for i, each in enumerate(data):
            # data[i] = list(each)
            tmp = []
            for j in each:
                tmp.append(each[j])
            data_dict[i] = tmp
        return data_dict