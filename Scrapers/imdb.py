import requests
from bs4 import BeautifulSoup
import re

class ImdbScraper:
    
    def __init__(self) -> None:
        self.search_query_results = {}
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Connection': 'close'
        }

    def preform_search_query(self, query: str) -> dict:
        """Preforms a search query on TMDB's website using their standard peremeters. 
        IE., if TMDB thinks you're searching for a tv show, this method will think you're searching for a tv show

        Args:
            query (str): Desired search term. Will be added to the end of the string " https://www.themoviedb.org/search?query={query} "

        Returns:
            dict: Sets self.search_query_results and returns a dictionary of filled values. 
            The values of the dictionary are [show_name, release_date, show_desc, thumbnail, link]
        """
        page = requests.get(f"https://www.imdb.com/find?q={query}&s=tt&ref_=fn_tt", headers=self._headers)
        page = BeautifulSoup(page.text, "html.parser")        
        content = page.find_all("tr", {'class' : ['findResult odd', 'findResult even']}) # samples 20 from the tv shows and movies section. TMDB decision, not mine. Hardcorded limit to remove weirdness
        tmp = {}
        print(f"{len(content)} results")
        x=0
        for each in content:
            each = str(each)
            print(each)
            # exit(0)
            x += 1
            if x == 2:
                break
            info = []
            # info.append(re.search(r'(?<=h2>)([^<]+)', each)[0]) # show name
            # release_date = re.search(r'(?<=date">)([^<]+)', each)
            # info.append("") if release_date is None else info.append(release_date[0])
            # show_desc = re.search(r'(?<=<p>)([^<]+)', each)
            # info.append("") if show_desc is None else info.append(show_desc[0])
            # thumbnail = re.search(r'(?<=src=")([^"]+)', each)
            # info.append("") if thumbnail is None else info.append(thumbnail[0])
            # info.append(re.search(r'(?<=href=")([^"]+)', each)[0]) # show link
            # tmp[len(tmp)] = info
            # if len(tmp) == 20: # If it can't be found within the first 20 guesses, they should try a better query
                # break
        for x in range(len(tmp)):
            print(tmp[x][0])
        self.search_query_results = tmp
        return self.search_query_results

if __name__ == '__main__':
    tmp = ImdbScraper()
    tmp = tmp.preform_search_query('survivor')