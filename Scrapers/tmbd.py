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

        self.search_query_results = {}


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

    def preform_search_query(self, query: str) -> dict:
        """Preforms a search query on TMDB's website using their standard peremeters. 
        IE., if it thinks you're searching for a tv show, this method will think you're searching for a tv show

        Args:
            query (str): Desired search term. Will be added to the end of the string " https://www.themoviedb.org/search?query={query} "

        Returns:
            dict: Sets self.search_query_results and returns a dictionary of filled values. 
            The values of the dictionary are [show_name, release_date, show_desc, thumbnail, link]
        """
        page = requests.get(f"https://www.themoviedb.org/search?query={query}", headers=self._headers)
        page = BeautifulSoup(page.text, "html.parser")        
        content = page.find_all("div", class_='card v4 tight') # samples 20 from the tv shows and movies section. TMDB decision, not mine. Hardcorded limit to remove weirdness
        tmp = {}
        for each in content:
            each = str(each)

            info = []

            info.append(re.search(r'(?<=h2>)([^<]+)', each)[0]) # show name
            release_date = re.search(r'(?<=<p>)([^<]+)', each)
            info.append(None) if release_date is None else info.append(release_date[0])
            show_desc = re.search(r'(?<=<p>)([^<]+)', each)
            info.append(None) if show_desc is None else info.append(show_desc[0])
            thumbnail = re.search(r'(?<=<p>)([^<]+)', each)
            info.append(None) if thumbnail is None else info.append(thumbnail[0])
            info.append(re.search(r'(?<=href=")([^"]+)', each)[0]) # show link

            tmp[len(tmp)] = info
            if len(tmp) == 20: # If it can't be found within the first 20 guesses, they should try a better query
                break
        self.search_query_results = tmp
        return self.search_query_results

    def get_season(self, tmdbID: str):
        """_summary_

        Args:
            tmdbID (str): _description_
        """
        pass

if __name__ == '__main__':
    # test = requests.get("https://www.themoviedb.org/")
    pass