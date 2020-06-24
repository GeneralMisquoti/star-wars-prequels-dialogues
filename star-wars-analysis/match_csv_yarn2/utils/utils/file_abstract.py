from pathlib import Path
from typing import Iterable, Callable, List, Union, Type, Dict

from .row_abstract import Row
from .utils.sentence import Sentence
from ..overrides import Overrides
from ..row_csv import CsvRow
from ..row_json import JsonRow


class Movie:
    def __init__(self, name: str, index: int, overrides: Overrides = None):
        self.overrides = overrides
        self.name = name
        self.index = index
        self.sentences: List[Sentence] = []
        self.rows: List[Row] = []

    def make_list(
            self,
            list_of_dialogues: Iterable[Union[Iterable[str], Dict[int, str]]],
            creator: Type[Union[JsonRow, CsvRow]]
    ):
        max_id = 0

        row_offset = 0
        sentence_offset = 0
        for i, row in enumerate(list_of_dialogues):
            last_row = creator(
                row,
                max_id,
                index=i,
                row_offset=row_offset,
                sentence_offset=sentence_offset
            )
            max_id = last_row.sentences[-1].id + 1
            self.rows.append(last_row)
            self.sentences.extend(last_row)

            if not self.overrides:
                continue

            should_insert = self.overrides.should_insert(last_row)
            if should_insert:
                for insert_instruction in should_insert:
                    new_row = creator(
                        insert_instruction.raw_csv_data(),
                        max_id,
                        index=i,
                        row_offset=row_offset,
                        sentence_offset=sentence_offset,
                        offset=True
                    )
                    row_offset += 1
                    new_max_id = new_row.sentences[-1].id + 1
                    sentence_offset += new_max_id - max_id
                    max_id = new_max_id
                    self.rows.append(new_row)
                    self.sentences.extend(new_row)


class File:
    def __init__(self, path: Path, movie_index: int, overrides: Overrides = None):
        self.path = path
        self.movie = Movie(name=path.name, index=movie_index, overrides=overrides)
        self._iter = self.movie.sentences

    def parse(self, list_of_dialogues: Iterable[Iterable[str]], creator: Callable):
        self.movie.make_list(list_of_dialogues, creator)
