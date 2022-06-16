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
    
    def test_query_results_single_result(self): # this will pull from both tv shows and movies. while there is only 1 show, there are 3 movies, resulting in 4 total
        tmp = TmbdScraper()
        tmp = tmp.preform_search_query('moon knight')
        self.assertEqual(len(tmp), 4) # we hardcord it so that only 20 search results come back
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)

if __name__ == '__main__':
    unittest.main()
