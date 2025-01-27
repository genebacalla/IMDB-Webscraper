# (1) highest rated movie in 2023               -> bayesian_rating_average
# (2) most popular actor in 2023                -> pca 
# (3) highest rated movie over the year         -> bayesian_rating_average + metacriticscore
# (4) what is a hit movie? define the metrics.  -> bayesian_rating_average + metacriticscore + awards_nominees + budget + textblob sentiminent analysis

import requests
import json
import re   
from bs4 import BeautifulSoup 
from SeleniumScraper import getAwardsPage

class WebScraper:

    def __init__ (self, tconst):
        self.tconst = tconst

        print("[LOGS]: CONFIGURATION LOADING STARTED...")
        self.webpages = self.dict_tags = None
        
        with open("webpages.json", "r") as json_file:
            _webpages = json.load(json_file)
            
        with open("awards.json", "r") as json_file:
            self.dict_tags = json.load(json_file)
   
        self.webpages = [s.replace("{tconst}", self.tconst) for s in _webpages]

        if len(self.webpages) != 0 and len(self.dict_tags) != 0:
            print("[LOGS]: CONFIGURATION LOADING SUCCESS.")
        else:
            print("[LOGS]: CONFIGURATION LOADING FAILED.")
            return None
        


    def _apply_element_filter(self, current_soup, key, value):
        next_soup = []
        for element in current_soup:
            if key == 'class':
                filtered = element.find_all(class_=value)
            elif key == 'data-testid':
                filtered = element.find_all(attrs={key: value})
            else:
                return None
            next_soup.extend(filtered)
        return next_soup
    
    def _parse_tags(self, soup, payload):
        current_soup = [soup]  
        for key, value in payload.items():
            current_soup = self._apply_element_filter(current_soup, key, value)
            if not current_soup:
                return None
        return current_soup

    def _identify_award(self, award):
        _wins_count = _nominees_count = _oscar_nominees_count = _oscar_wins_count = 0   
        award = award.text
        if 'Oscar' in award and 'Nominee' in award:
            _oscar_nominees_count+=1
        elif 'Oscar' in award and 'Winner' in award:
            _oscar_wins_count+=1
        elif 'Nominee' in award:
            _nominees_count+=1
        elif 'Winner' in award:
            _wins_count+=1     

        return [_wins_count, _nominees_count, _oscar_wins_count, _oscar_nominees_count]  
        
    def _filter_movie_awards(self, awards_list):
            _wins_count = _nominees_count = _oscar_nominees_count = _oscar_wins_count = 0
            for awards in awards_list:
                _award = self._identify_award(awards)  
                _wins_count += _award[0]
                _nominees_count += _award[1]
                _oscar_wins_count += _award[2]
                _oscar_nominees_count += _award[3]
                
            return [_wins_count, _nominees_count, _oscar_wins_count, _oscar_nominees_count]  
     
    def get_movie_metacritic_score(self):
        success, soup = self.fetch_url(self.webpages[0])
        if success:
            try:
                return self._parse_tags(soup, self.dict_tags[1])[0].text
            except:
                return None
        else:
            return None
        
    def fetch_url(self, imdb_url):
        response = requests.get(imdb_url, headers = self.dict_tags[0])
        if response.status_code == 200:
            return True, BeautifulSoup(response.content, "html.parser")
        else:
            return False, None
        
    def get_movie_awards(self):
        soup = getAwardsPage() 
        try:
            return self._filter_movie_awards(self._parse_tags(soup, self.dict_tags[2]))
        except:
            return None
        
    def get_movie_budget(self):
        success, soup = self.fetch_url(self.webpages[0])
        if success:
            try:
                return re.sub(r'\D', '', self._parse_tags(soup, self.dict_tags[3])[0].text)
            #numeric_string = re.sub(r'\D', '', string)
            except:
                return None
        else:
            return None
                
    def get_movie_gross_worldwide(self):
        success, soup = self.fetch_url(self.webpages[0])
        if success:
            try:
                return re.sub(r'\D','',self._parse_tags(soup, self.dict_tags[4])[0].text)
            except:
                return None
        else:
            return None
        
tconst = "tt15398776"

scraper = WebScraper(tconst)

print("***************************************************")
print("                  UNIT TESTING                     ")
print("***************************************************")
print("tconst: ", tconst)
print("metacritic: ", scraper.get_movie_metacritic_score())
print("moviebudget: ", scraper.get_movie_budget())
print("grossworldwide: ", scraper.get_movie_gross_worldwide())
print("awards: ", scraper.get_movie_awards())
print("***************************************************")
#scraper._get_principal_credit()
#scraper.get_director()