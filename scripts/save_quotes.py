import json
from typing import List
from json import JSONEncoder

from quote import SerializeQuote
from movies import WhichMovie, movie_dict
from here import here

parsed_scripts = here / "parsed_scripts"
if not parsed_scripts.exists() or not parsed_scripts.is_dir():
    parsed_scripts.mkdir()


class MyEncoder(JSONEncoder):
    def default(self, o):
        return {k: v for k, v in o.__dict__.items() if k[0] != '_'}


def save_quotes(movie: WhichMovie, characters, quotes: List[SerializeQuote]):
    json.dump(
        {'characters': characters, 'quotes': quotes},
        (parsed_scripts / (movie_dict[movie] + '.json')).open('w+', encoding='UTF-8'),
        ensure_ascii=False,
        cls=MyEncoder
    )
