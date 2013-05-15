import requests
import csv

IMDBAPI = "http://imdbapi.org/"
OMDBAPI = "http://www.omdbapi.com/"
ROTTENAPI = "http://api.rottentomatoes.com/api/public/v1.0/"

R_API_KEY = "bgqqqdtscv9hdce67yekfufm"


class Movies(object):
    """client for diverse movie APIs"""
    def __init__(self):
        self.max_id = 2400000

    def search_by_id(self, id):
        r = requests.get(IMDBAPI + "?id=" + id)
        return r.json()

    def search_results_by_name(self, query):
        r = requests.get(OMDBAPI + "?s=" + query)
        return r.json()

    def search_by_name(self, name):
        r = requests.get(IMDBAPI + "?q=" + name)
        return r.json()

    def search_by_name_R(self, name):
        r = requests.get(ROTTENAPI + "movies.json?apikey=" + R_API_KEY +
            "&q=" + name + "&page_limit=1")
        return r.json()

    def imdb_top250(self):
        r = requests.get("http://app.imdb.com/chart/top")
        movies = r.json()['data']['list']['list']
        return movies

    def imdb_worst100(self):
        r = requests.get("http://app.imdb.com/chart/bottom")
        return r.json()

    def create_movie_db(self):
        topmovies = self.imdb_top250()
        data = []
        for movie in topmovies:
            try:
                movie_bis = self.search_by_name(movie['title'])
                new_entry = {'title': movie['title'], 'rating': movie['rating'],
                             'year': movie['year'], 'imdb_url': movie_bis[0]['imdb_url'],
                             'poster': movie_bis[0]['poster'],
                             'plot': movie_bis[0]['plot_simple']}
                data.append(new_entry)
            except (KeyError, ValueError):
                pass

        with open('moviedb.csv', 'w') as csvfile:
            fieldnames = ('title', 'rating', 'year',
                          'imdb_url', 'poster', 'plot')
            f = csv.DictWriter(csvfile, fieldnames)
            f.writerows(data)


class Parser(object):
    """Extract features from movie data"""
    def __init__(self):
        pass

    def parse(self, imdb_mov, rt_mov):
        title, rating = imdb_mov['title'], imdb_mov['rating']
        try:
            img = rt_mov['movies'][0]['posters']['original'] \
             or "No image available"
            text = rt_mov['movies'][0]['synopsis'] or \
             rt_mov['movies'][0]['critics_consensus'] or "Summary not available"
        except KeyError:
            pass

        return (title, rating, img, text)
