from pathlib import Path
from typing import Iterable, Callable, List, Union, Type

from .row_abstract import Row
from .utils.sentence import Sentence


class Movie:
    def __init__(self, name):
        self.name = name
        self.sentences: List[Sentence] = []
        self.rows: List[Row] = []

    def make_list(self, list_of_dialogues: Iterable, creator: Type[Row]):
        max_id = 0
        for row in list_of_dialogues:
            last_row = creator(row, max_id)
            max_id = last_row.sentences[-1].id + 1
            self.rows.append(last_row)
            self.sentences.extend(last_row)


class File:
    def __init__(self, path: Path):
        self.path = path
        self.movie = Movie(name=path.name)
        self._iter = self.movie.sentences

    def parse(self, list_of_dialogues: Iterable, creator: Callable):
        self.movie.make_list(list_of_dialogues, creator)
