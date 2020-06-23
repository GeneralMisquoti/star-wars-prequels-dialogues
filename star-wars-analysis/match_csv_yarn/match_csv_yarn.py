from pathlib import Path
from pprint import pprint
from fuzzywuzzy import fuzz
from typing import List, Optional, Callable, Union, Iterable, Tuple
import json
import csv
from itertools import groupby

here = Path(__file__).parent
output_path = here / "output"


class _File:
    def __init__(self, path: Path):
        self.path = path


class Match:
    def __init__(self, json_row=None, ratio=None, csv=None):
        self.json_row: JsonQuote = json_row
        self.ratio = ratio
        self.csv = csv

    def __repr__(self):
        return f'<Match {self.json_row.__repr__()}>'

    """
    Matched ['Use caution.', 'These Jedi are not to be underestimated.']:
    [<Match <JsonQuote transcript="Use caution. These Jedi are not to be underestimated.">>,
     <Match <JsonQuote transcript="If they're down here, sir, we'll find them.">>]
    """
    def set(self):
        pass


class CsvRow:
    def __init__(self, row: List[str], i: int):
        self.speaker = row[0]
        self.addressed = row[1]
        # self.lineorder = int(row[2])
        self.i = i
        self.combinedline = row[3]
        self.split_line = self._split_row(self.combinedline)
        self.numberofrows = row[4]
        self.wordcount = row[5]
        self.match: Optional[List[Match]] = None
        self.blacklisted = False

    def set_match(self, _match: List[Match]):
        self.match = _match

    def to_json(self):
        matches = []
        if self.match:
            for _match in self.match:
                rv = self.combinedline.find(_match.csv)
                if rv == -1:
                    rv = self.combinedline.find(_match.csv[:-1])
                    if rv == -1:
                        print(f"Error matching substring in {self}")
                        return
                matches.append(((rv, len(_match.csv)), _match.csv, _match.json_row.transcript, _match.json_row.id))
        return {
            'from': self.speaker,
            'to': self.addressed,
            'id': self.i,
            'transcript': self.combinedline,
            'numberofrows': self.numberofrows,
            'matches': matches,
        }

    def _split_row(self, row: str) -> List[str]:
    # def _split_row(self, row: str) -> List[Tuple[int, int]]:

        # def split_with_indices(start: int, end: int, row: str, c=' '):
        #     """ https://stackoverflow.com/questions/13734451/string-split-with-indices-in-python """
        #     s = row[start:end]
        #     if c not in s:
        #         yield start, end
        #         return
        #     p = 0
        #     for k, g in groupby(s, lambda _x: _x == c):
        #         q = p + sum(1 for i in g)
        #         if not k:
        #             yield p, q
        #         p = q
        #
        # def strip(start: int, end: int, str: str):
        #     removed_from_the_left = str.lstrip()
        #     start += len(removed_from_the_left) - len(str)
        #     removed_from_the_right = str.rstrip()
        #     if removed_from_the_right[-3:] == "...":
        #         removed_from_the_right = removed_from_the_right[:-3]
        #
        #     end -= len(removed_from_the_right) - len(str)
        #     return start, end
        #
        # splitters = ['.', '!', '?']
        # split = [(0, len(row))]
        # for splitter in splitters:
        #     new_split = []
        #     for already_start, already_end in split:
        #         already_split = row[already_start:already_end]
        #         already_start, already_end = strip(already_start, already_end, already_split)
        #         new_new_split = list(split_with_indices(already_start, already_end, row, c=splitter))
        #         if new_new_split == split:
        #             continue
        #         for x_start, x_end in new_new_split:
        #             x_start, x_end = strip(x_start, x_end, row[x_start:x_end])
        #             if x_end - x_start != 0:
        #                 if row[x_end] in splitters:  # 'Yes, Master. How do you think this trade viceroy will deal with the chancellor\'s demands?'
        #                     new_split.append((x_start, x_end+1))
        #                 else:
        #                     new_split.append((x_start, x_end+1))
        #     if len(new_split) != 0:
        #         split = new_split
        # test_split = [row[s:e] for s, e in split]
        # return split
        splitters = ['.', '!', '?']
        split = [row]
        for splitter in splitters:
            new_split = []
            for already_split in split:
                new_new_split = already_split.strip().split(splitter)
                if new_new_split == split:
                    continue
                for x in new_new_split:
                    x_strip = x.strip()
                    if len(x_strip) != 0:
                        if x_strip[-1] in splitters:  # 'Yes, Master. How do you think this trade viceroy will deal with the chancellor\'s demands?'
                            new_split.append(x_strip)
                        else:
                            if x_strip[-1] != ',':
                                new_split.append(f'{x_strip}{splitter}')
                            else:
                                new_split.append(x_strip)
            if len(new_split) != 0:
                split = new_split
        return split

    def __repr__(self):
        return f'<CsvRow from="{self.speaker}" line="{self.combinedline}">'


class CsvFile(_File):
    CSV_BLACKLIST = [
        "BEEPS TWICE",
        "BEEPS THREE TIMES",
        "[ Beeping ]",
        "[ Chirping ]",
        "[Whistles, Beeps ]",
        "[ Beeping ] [ Beeping ]",
        "[ Whistling, Beeping ]",
        "[ Raspberries ]",
        "[ Beeping ] [ Whistling ]",
        "[ Beeping, Chirping ]",
        "Whoa, whoa. Oh, whoa!"  # FIXME: Include these blacklisted phrases anyway without a yarn id!
    ]
    CSV_BLACKLIST_IDS = [
        [],
        [413, 415, 416],
        []
    ]

    def __init__(self, path: Path, name="", i=None):
        super().__init__(path)
        self.rows: List[CsvRow] = []
        with self.path.open('r', encoding="UTF-8") as _file:
            csv_reader = csv.reader(_file, quotechar='"', delimiter=',')
            csv_reader.__next__()
            for i, _row in enumerate(csv_reader):
                new_row = CsvRow(_row, i)
                if new_row.combinedline in self.CSV_BLACKLIST:
                    new_row.blacklisted = True
                if new_row.i in self.CSV_BLACKLIST_IDS[i]:
                    new_row.blacklisted = True
                self.rows.append(new_row)
            self.rows = self.rows[1:]

    def __iter__(self) -> Iterable[CsvRow]:
        for _row in self.rows:
            yield _row


class JsonQuote:
    def __init__(self, json_obj, i: int):
        self._json_obj = json_obj
        self.id = json_obj['id']
        self.transcript = json_obj['transcript']
        self.index = i

    def __repr__(self):
        return f'<JsonQuote transcript="{self.transcript}">'


class JsonFile(_File):

    def __init__(self, path: Path, i=None):
        super().__init__(path)
        self.previous_i: int = 0
        self.quotes: List[JsonQuote] = []
        with self.path.open('r', encoding="UTF-8") as _file:
            self._json_file = json.load(_file)
            for i, _row in enumerate(self._json_file):
                self.quotes.append(JsonQuote(_row, i))

    """Called for each csv row when reading files"""
    def match(self, _csv_row: List[str]) -> Optional[List[Match]]:
        searched_for = _csv_row

        # searched_for = _csv_row.combinedline
        # matches: List[Match] = []
        searched_range = range(len(searched_for))
        # [0] == "Use caution.", 'Yousa follow me now, okeyday?'
        matches: List[Optional[Match]] = [None for _ in searched_range]
        is_matched: List[bool] = [False for _ in searched_range]

        for j, json_row in enumerate(self.quotes[self.previous_i:]):
            for i, _s in enumerate(searched_for):
                if is_matched[i]:
                    continue
                match_ratio = fuzz.token_set_ratio(_s, json_row.transcript)  # https://www.datacamp.com/community/tutorials/fuzzy-string-python
                _match = Match(ratio=match_ratio, json_row=json_row, csv=_s)
                if matches[i] is None:
                    matches[i] = _match
                elif j > i + 5 and matches[i].ratio > match_ratio:
                    print("Previous match better than present. Abort.")
                    is_matched[i] = True
                    matches[i].set()
                    continue
                else:
                    if matches[i].ratio < _match.ratio:
                        matches[i] = _match
                if _match.ratio >= 95:
                    is_matched[i] = True
                    matches[i].set()
            if all(is_matched):
                break

        if not any(matches):
            return None
        min_match = max(filter(lambda m: m is not None, matches), key=lambda m: m.json_row.index)
        self.previous_i = min_match.json_row.index
        return matches


class Data:
    data: Path
    data_files: Optional[List[Union[CsvFile, JsonFile]]]
    _data_files: List[str]  # paths relative to data: Path
    _file_creator: Callable[[Path], Union[CsvFile, JsonFile]]

    def iter_files(self):
        for _iter in self.data_files:
            yield _iter

    def create_files(self):
        new_files = []
        for i, _file in enumerate(self._data_files):
            new_path = self.data / _file
            new_path = self._file_creator(new_path, i=i)
            new_files.append(new_path)
        return new_files

    def __init__(self):
        self.data_files = self.create_files()


class CsvData(Data):
    """
    courtesy Sean Green et al.
    https://github.com/datadesk/star-wars-analysis
    """
    data = here.parent / "data"
    _data_files: List[str] = ["01_phantom_menace.csv", "02_attack_of_the_clones.csv", "03_revenge_of_the_sith.csv"]
    data_files: List[CsvFile]
    _file_creator: Callable[[Path], CsvFile] = CsvFile


class JsonData(Data):
    """
    Yarn Json Data
    """
    data = here.parent.parent / "yarn" / "parsing_source" / "parsed_sources" / "hand_fixed"
    _data_files: List[str] = ["phantom_menace.json", "attack_of_the_clones.json", "revenge_of_the_sith.json"]
    data_files: List[JsonFile]
    _file_creator: Callable[[Path], CsvFile] = JsonFile


if __name__ == "__main__":
    if not output_path.exists():
        output_path.mkdir()
    csv_data = CsvData()
    json_data = JsonData()
    for csv_file, json_file in zip(csv_data.iter_files(), json_data.iter_files()):
        csv_file: CsvFile
        json_file: JsonFile
        for csv_row in csv_file:
            if csv_row.blacklisted:
                continue
            searched_for = csv_row.split_line

            match = json_file.match(searched_for)
            if match is None:
                print(f'{csv_row.i}: Not found any matches for "{searched_for}"')
            else:
                # print(f'{csv_row.i}: Matched "{searched_for}":\n"{match}\n"')
                csv_row.set_match(match)

        new_file_name = json_file.path.name
        file_output_path = output_path / new_file_name
        json.dump([row.to_json() for row in csv_file.rows], file_output_path.open('w+', encoding="UTF-8"), ensure_ascii=False)

