'''
File will handle interactions for https://www.themoviedb.org/
'''

import requests
from bs4 import BeautifulSoup
import re

class TmbdScraper:

    def __str__(self) -> str:
        return f"{self.season_info}"

    def __init__(self) -> None:
        
        self.season_info = {}
        """dict: 
            
            Key (int): season number

            Value (list): []
            
        """
        self.popular_page = {}

        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Connection': 'close'
        }

    def clear(self):
        self.season_info = {}
        self.popular_page = {}

    def get_popular_movies(self) -> dict:
        url = "https://www.themoviedb.org/movie"
        return self._get_popular_page_info(url)

    def get_popular_tv_shows(self) -> dict:
        url = "https://www.themoviedb.org/tv"
        return self._get_popular_page_info(url)

    def _get_popular_page_info(self, url) -> dict:
        if self.popular_page:
            self.popular_page = {}
        page = requests.get(url, headers=self._headers)
        page = BeautifulSoup(page.text, "html.parser")
        # test = page.find_all("div", {"class": ["image", "content"]})
        for each in page.find_all("div", class_="card style_1"):
            each = str(each)
            info = []
            info.append(re.search(r'(?<=title=")([^"]+)', each)[0]) # show title
            info.append(re.search(r'(?<=<p>)([^<]+)', each)[0]) # release date
            info.append(re.search(r'(?<=percent=")([^"]+)', each)[0]) # show rating
            info.append('https://www.themoviedb.org' + re.search(r'(?<=href=")(/[^"]+)', each)[0]) # link to page
            info.append('https://www.themoviedb.org' + re.search(r'(?<=src=")([^"]+)', each)[0]) # img thumbnail
            self.popular_page[len(self.popular_page)] = info
        return self.popular_page

    def get_season(self, tmdbID: str):
        """_summary_

        Args:
            tmdbID (str): _description_
        """
        pass

if __name__ == '__main__':
    # test = requests.get("https://www.themoviedb.org/")
    pass