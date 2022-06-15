import unittest
from Scrapers.tmbd import TmbdScraper

class Test(unittest.TestCase):
    
    def test_popular_movies(self):
        tmp = TmbdScraper()
        tmp = tmp.get_popular_movies()
        self.assertEqual(len(tmp), 20) # default view by tmdb is 20
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)
        print(tmp)
    
    def test_popular_tv_shows(self):
        tmp = TmbdScraper()
        tmp = tmp.get_popular_tv_shows()
        self.assertEqual(len(tmp), 20) # default view by tmdb is 20
        for x in range(len(tmp)): # make sure each list has 5 entries
            self.assertEqual(len(tmp[x]), 5)
    


if __name__ == '__main__':
    unittest.main()
