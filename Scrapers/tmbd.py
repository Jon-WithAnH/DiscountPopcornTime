'''
File will handle interactions for https://www.themoviedb.org/
'''

import requests
from bs4 import BeautifulSoup
import re

class TmbdScraper:
    """Object used for parsing https://www.themoviedb.org/
    """
    def __str__(self) -> str:
        return f"{self.season_info}"

    def __init__(self) -> None:
        
        self.season_info = {}
        """
        dict: 
            Key (int): season number
            Value (list): [show_name, release_date, show_desc, thumbnail, link]
        """
        self.popular_page = {}
        """
        dict: 
            Key (int): Number placement on the popular page
            Value (list): []
        """

        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Connection': 'close'
        }

        self.search_query_results = {}
        """
        dict:
            Key values are in the order of: [show_name, release_date, show_desc, thumbnail, link]
        """
        self.seasons = {}
        self.episode_listing = {}


    def clear(self):
        self.season_info = {}
        self.popular_page = {}

    def get_popular_movies(self) -> dict:
        """_summary_

        Returns:
            dict: Information about each title on the popular page.
            Each key has the value in the order: [show_title, release_date, show_rating, thumbnail, link]
        """
        url = "https://www.themoviedb.org/movie"
        return self.__get_popular_page_info(url)

    def get_popular_tv_shows(self) -> dict:
        url = "https://www.themoviedb.org/tv"
        return self.__get_popular_page_info(url)

    def __get_popular_page_info(self, url: str) -> dict:
        """Internally used

        Args:
            url (str): _description_

        Returns:
            dict: Information about each title on the popular page.
            Each key has the value in the order: [show_title, release_date, show_rating, thumbnail, link]
        """
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
            thumby = re.search(r'(?<=src=")([^"]+)', each)
            if thumby: 
                # info.append('https://www.themoviedb.org' + thumby[0]) # img thumbnail
                info.append(thumby[0]) 
            else:
                info.append("")
            # info.append('https://www.themoviedb.org' + re.search(r'(?<=href=")(/[^"]+)', each)[0]) # link to page
            info.append(re.search(r'(?<=href=")(/[^"]+)', each)[0]) # link to page
            self.popular_page[len(self.popular_page)] = info
        return self.popular_page

    def preform_search_query(self, query: str) -> dict:
        """Preforms a search query on TMDB's website using their standard peremeters. 
        IE., if TMDB thinks you're searching for a tv show, this method will think you're searching for a tv show

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
            release_date = re.search(r'(?<=date">)([^<]+)', each)
            info.append("") if release_date is None else info.append(release_date[0])
            show_desc = re.search(r'(?<=<p>)([^<]+)', each)
            info.append("") if show_desc is None else info.append(show_desc[0])
            thumbnail = re.search(r'(?<=src=")([^"]+)', each)
            info.append("") if thumbnail is None else info.append(thumbnail[0])
            info.append(re.search(r'(?<=href=")([^"]+)', each)[0]) # show link
            tmp[len(tmp)] = info
            if len(tmp) == 20: # If it can't be found within the first 20 guesses, they should try a better query
                break
        # for x in range(len(tmp)):
            # print(tmp[x][0])
        self.search_query_results = tmp
        return self.search_query_results

    def get_season(self, tmdbID: str) -> dict|None:
        """Gets all seasons and season descriptions of the given show

        Args:
            tmdbID (str): The str provided by TMDB through their link page. Format: /tv/14658
        Returns:
            dict: Sets self.seasons and returns a dictionary of filled values. 
            None if the query is not valid for seasons. IE., it's a movie or an anime (not supported).
            The values of the dictionary are [season_name, release_date (WARN: Eg. "2020 | 1 Episode"), season_desc, thumbnail, link].
        """
        ## Check ID to make sure it's not a movie
        if not tmdbID.__contains__("tv"):
            raise Exception("in tmdb.py get_season(): Attempted to get info for non-valid link")
        seasons = {}
        # https://www.themoviedb.org/tv/14658-survivor/seasons
        tmdbID = tmdbID.split("/") # ['', 'tv', '14658']
        page = requests.get(f"https://www.themoviedb.org/tv/{tmdbID[-1]}/seasons", headers=self._headers)
        page = BeautifulSoup(page.text, "html.parser")
        # print(page)  
        content = page.find_all("div", class_='season') 
        # print(f"{len(content)} results")
        for each in content:
            # print(each)
            each = str(each)
            info = []
            info.append(re.search(r'(?<=">)([^<|\n]+)', each)[0]) # season name
            release_date = re.search(r'(?<=<h4>)([^<]+)', each) # Eg. "2020 | 1 Episode"
            info.append("") if release_date is None else info.append(release_date[0])
            season_desc = re.search(r'(?<=<p>)([^<]+)', each) # season desc
            info.append("") if season_desc is None else info.append(season_desc[0])
            thumbnail = re.search(r'(?<=src=")([^"]+)', each)
            info.append("") if thumbnail is None else info.append(thumbnail[0])
            info.append(re.search(r'(?<=href=")([^"]+)', each)[0]) # show link
            seasons[len(seasons)] = info
        

        self.seasons = seasons
        return self.seasons

    def get_episodes(self, tmdbID: str) -> dict:
        """Gets all infomation about the given season for a given show

        Args:
            tmdbID (str): The str provided by TMDB through their link page. Format: /tv/14658-survivor/season/42
        Returns:
            dict: Sets self.episode_listing and returns it. 
            The values of the dictionary are [season_number, episode_title, release_date, episode_duration, episode_desc, thumbnail, link]
        """
        # https://www.themoviedb.org/tv/14658-survivor/season/42
        # /tv/14658-survivor/season/42
        results = {}
        page = requests.get(f"https://www.themoviedb.org{tmdbID}", headers=self._headers)
        page = BeautifulSoup(page.text, "html.parser")
        content = page.find_all("div", class_='card') 
        # print(f"{len(content)} episode results for {tmdbID}")  

        for each in content:
            each = str(each)
            info = []
            info.append(re.search(r'(?<=season=")([^"]+)', each)[0]) # season_number
            info.append(re.search(r'(?<=">)([^"]+)(?=</a><)', each)[0]) # episode_title
            info.append(re.search(r'(?<=<span>)([^<]+)', each)[0]) # release_date
            info.append(re.search(r'(?<=<span>)([^<]+)', each)[1]) # episode_duration
            info.append(re.search(r'(?<=<p>)([^<]+)', each)[0]) # episode_desc
            thumbnail = re.search(r'(?<=src=")([^"]+)', each)
            info.append("") if thumbnail is None else info.append(thumbnail[0])
            info.append(re.search(r'(?<=href=")([^"]+)', each)[0]) # episode link
            results[len(results)] = info

        self.episode_listing = results
        return self.episode_listing


if __name__ == '__main__':
    # test = requests.get("https://www.themoviedb.org/")
    tmp = TmbdScraper()
    tmp.get_season("/tv/14658")