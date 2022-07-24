from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from Pages.ExtendedFunctions import WrappedLabel, CustomButton, DBButton, SubmitButton
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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
            float_test = FloatLayout()
            if not data[each][3] == "":
                # Reaplacing the size of the images to match the images from the front page
                # https://www.themoviedb.org/t/p/w94_and_h141_bestv2/5R125JAIh1N38pzHp2dRsBpOVNY.jpg
                # https://www.themoviedb.org/t/p/w220_and_h330_face/9HFFwZOTBB7IPFmn9E0MXdWave3.jpg
                data[each][3] = data[each][3].replace("94", "220")
                data[each][3] = data[each][3].replace("141", "330")
                thumby = 'https://www.themoviedb.org' + data[each][3]  
                float_test.add_widget(AsyncImage(source=thumby, pos_hint={"center_x": .5, "center_y": .5}))
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
            level_3.add_widget(SubmitButton(data[each][4], text='Select')) # TODO on_press=selected_content
            level_2.add_widget(level_3)
            parent.add_widget(level_2)
        self.add_widget(parent)
        return parent  

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