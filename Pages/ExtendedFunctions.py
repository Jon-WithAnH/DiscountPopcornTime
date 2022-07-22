from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage

from sql.SqlManager import SqlContextManager

class SubmitButton(Button):
    """Button used when the user is ready to open a link to whatever they want to watch"""
    def __init__(self, data: str, **kwargs):
        """Create a button to use that will assemble the link to fsapi

        Args:
            data (str): postfix of tmdb link. IE., /tv/14658-survivor/season/42/episode/1 OR /movie/507086
        """
        super().__init__(**kwargs)
        self.data = data

    def on_press(self):
        # https://fsapi.xyz/tmdb-movie/{TMDb_ID}
        # or
        # https://fsapi.xyz/tv-tmdb/{TMDb_ID}-{SEASON_NUMBER}-{EPISODE_NUMBER}
        if self.data.__contains__("movie"):
            self.__generate_movie_link()
        else:
            self.__generate_episode_link()
        # Episode selection
        return super().on_press()
    
    def __generate_episode_link(self):
        # Episode selection
        # /tv/14658-survivor/season/42/episode/1
        info = self.data.split("/")
        ep_num = info[-1]
        season_num = info[-3]
        tmdb_num = info[2] # 14658-survivor
        tmdb_num = tmdb_num.split("-")[0]
        # URL: https://fsapi.xyz/tv-tmdb/{TMDb_ID}-{SEASON_NUMBER}-{EPISODE_NUMBER}
        print(f"https://fsapi.xyz/tv-tmdb/{tmdb_num}-{season_num}-{ep_num}")
    
    def __generate_movie_link(self):
        self.data = self.data.split("/")[-1]
        # https://fsapi.xyz/tmdb-movie/{TMDb_ID}
        print(f"https://fsapi.xyz/tmdb-movie/{self.data}")
        


class CustomButton(Button):
    """Class of button that is used for storing data which is used as a pipe for future buttons 

    Args:
        Button (_type_): _description_
    """
    def __init__(self, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link
    
    def on_press(self):
        pass
        # print(self.link)

class DBButton(Button):
    """Class used to associate a button with a table in the database"""
    def __init__(self, table_name: str, data: list, **kwargs):
        """Create a button connected to the database supplied by the arg

        Args:
            table_name (str): Name of the table the button is tied to. Check SqlContextManager.SUPPORTED_DB_TABLES_ALIAS for supported tables.
            data (list): All information concerning the media.
        """
        super().__init__(**kwargs)
        self.data = data
        self.size_hint = (None, .2)
        self.width = 30
        self.DB = None
        # We can infer which DB the button is connected to based on the saved text within the button.
        # To do that, we'll check to make sure the buttons have a text that's supported.
        # Raise an exception if the button's text doesn't match anything supported.

        for i, each in enumerate(SqlContextManager.SUPPORTED_DB_TABLES_ALIAS):
            if table_name == each:
                self.DB = SqlContextManager.SUPPORTED_DB_TABLES[i]

        if not self.DB:
            raise AttributeError(f"Invalid table name on DBButton. \nUnable to parse: \"{table_name}\" \
                                    \nSupported types are {SqlContextManager.SUPPORTED_DB_TABLES_ALIAS}")

        with SqlContextManager() as manager:
            if manager.search_table(self.DB, self.data):
                self.background_normal = 'Pages\\resources\\newbookmark.png'
            else: self.background_normal = 'Pages\\resources\\emptybookmark.png'

    
    def on_press(self):
        # print(f"Data to be saved: {self.data}")
        with SqlContextManager() as manager:
            if manager.search_table(self.DB, self.data):
                manager.delete(self.DB, self.data)
                self.background_normal = 'Pages\\resources\\emptybookmark.png'
                return
            manager.commit(self.DB, self.data)
            self.background_normal = 'Pages\\resources\\newbookmark.png'
            

class MyButton(ButtonBehavior, AsyncImage):
    def __init__(self, im, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.source = im

    def on_press(self):
        # self.source = 'atlas://data/images/defaulttheme/checkbox_on'
        pass

    def on_release(self):
        # self.source = 'atlas://data/images/defaulttheme/checkbox_off'
        pass

class WrappedLabel(Label):
    # Based on Tshirtman's answer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))