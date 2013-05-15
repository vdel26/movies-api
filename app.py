from flask import Flask, jsonify, url_for
from movies import Movies, Parser
import random
import os
from functools import wraps


app = Flask(__name__)

searcher = Movies()
top = searcher.imdb_top250()
parser = Parser()


@app.route("/top250", methods=['GET'])
def top250():
    return jsonify(list=top)


@app.route("/random", methods=['GET'])
def getmovie():
    movie = random.choice(top)
    movie_bis = searcher.search_by_name_R(movie['title'])
    title, rating, img, text = parser.parse(movie, movie_bis)
    return jsonify(title=title, rating=rating, poster=img, plot=text)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
