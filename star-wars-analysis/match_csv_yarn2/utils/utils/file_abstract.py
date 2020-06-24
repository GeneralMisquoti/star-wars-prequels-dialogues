from pathlib import Path
from typing import Iterable, Callable, List, Union, Type

from .row_abstract import Row
from .utils.sentence import Sentence


class Movie:
    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.sentences: List[Sentence] = []
        self.rows: List[Row] = []

    def make_list(self, list_of_dialogues: Iterable, creator: Type[Row]):
        max_id = 0
        for i, row in enumerate(list_of_dialogues):
            last_row = creator(row, max_id, index=i)
            max_id = last_row.sentences[-1].id + 1
            self.rows.append(last_row)
            self.sentences.extend(last_row)


class File:
    def __init__(self, path: Path, movie_index: int):
        self.path = path
        self.movie = Movie(name=path.name, index=movie_index)
        self._iter = self.movie.sentences

    def parse(self, list_of_dialogues: Iterable, creator: Callable):
        self.movie.make_list(list_of_dialogues, creator)
