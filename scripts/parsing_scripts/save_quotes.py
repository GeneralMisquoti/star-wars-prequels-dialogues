from quote import SerializeQuote
from movies import Movies, MovieData, WhichMovie, movie_dict
from typing import List
from parsing_scripts import here


def save_quotes(movie: WhichMovie, characters, quotes: List[SerializeQuote]):
    json(here / (movie + '.json')).open('r+', encoding='UTF-8')
    pass
