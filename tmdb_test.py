from re import T
import unittest

from Scrapers.tmbd import TmbdScraper


class Test(unittest.TestCase):
    
    def test_popular_movies(self):
        tmp = TmbdScraper()
        tmp = tmp.get_popular_movies()
        self.assertEqual(len(tmp), 20) # default view by tmdb is 20
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)
    
    def test_popular_tv_shows(self):
        tmp = TmbdScraper()
        tmp = tmp.get_popular_tv_shows()
        self.assertEqual(len(tmp), 20) # default view by tmdb is 20
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)
    
    def test_query_results(self):
        tmp = TmbdScraper()
        tmp = tmp.preform_search_query('survivor')
        self.assertEqual(len(tmp), 20) # we hardcord it so that only 20 search results come back
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)
    
    def test_query_results_single_result(self):
        tmp = TmbdScraper()
        tmp = tmp.preform_search_query('survivorman')
        self.assertEqual(len(tmp), 4) # this will pull from both tv shows and movies. while there is only 1 show, there are 3 movies, resulting in 4 total
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)

    def test_get_seasons(self):
        tmp = TmbdScraper()
        tmp = tmp.get_season("/tv/14658")
        self.assertEqual("", tmp[0][3])
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)       

    def test_get_episodes(self):
        tmp = TmbdScraper()
        tmp = tmp.get_episodes("/tv/14658-survivor/season/42") 
        self.assertEqual(len(tmp), 13)

if __name__ == '__main__':
    unittest.main()
