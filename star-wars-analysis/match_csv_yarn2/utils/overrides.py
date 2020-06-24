from pathlib import Path
import re
from typing import Dict, List, Optional, Callable, Any, Union
from .row_csv import CsvRow
from .row_json import JsonRow
from csv import reader
from .utils.utils.sentence import Sentence
from .utils.row_abstract import Row
import toml
import logging

module_logger = logging.getLogger(__name__)


class OverridePermission:
    def __init__(self, allow: bool = True, force_id: List[int] = None):
        self.allow = allow
        self.force_id = force_id
        if not allow and force_id:
            raise Exception("Can't both disallow and force a different id!")


OverridePermission.Allow = OverridePermission()
OverridePermission.Forbid = OverridePermission(allow=False)


class GlobalOverrideForFile:
    def __init__(self, blacklist_regexes=None, try_replace=None):
        if blacklist_regexes is None:
            blacklist_regexes = []
        self.regexes = [re.compile(regex) for regex in blacklist_regexes]

        if try_replace is None:
            try_replace = {}
        new_try_replace = {}
        for map in try_replace:
            new_try_replace[map['original']] = map['replace']
        self.try_replace = new_try_replace

    def should_try_replace(self, csv_sentence: Sentence) -> Optional[str]:
        for key in self.try_replace:
            if key in csv_sentence.sentence:
                return csv_sentence.sentence.replace(key, self.try_replace[key])


class GlobalOverride:
    """TOML overrides"""

    def __init__(self, path: Path):
        parsed_toml = toml.load(path.open('r', encoding='UTF-8'))
        self.csv = GlobalOverrideForFile(**parsed_toml.get('csv'))
        self.json = GlobalOverrideForFile(**parsed_toml.get('json'))


class CSVFile:
    def headers_same(self, assert_headers, headers):
        for (ah, actual) in zip(assert_headers,headers):
            assert ah == actual.strip()

    def __init__(self, path: Path, assert_headers: List[str], line_creator: Callable[[List[str]], Dict[int, Any]]):
        self.path = path
        self.io = path.open('r', encoding='UTF-8')
        self.csv = reader(self.io)
        headers = self.csv.__next__()
        self.headers_same(assert_headers, headers)
        self.override_data: Dict[int, OverridePermission] = {}
        for line in self.csv:
            if len(line) == 0:
                continue
            if line[0][0] == "#":
                # Comments
                continue
            rv = line_creator(line)
            self.override_data = {**self.override_data, **rv}

        self.io.close()


class CSVOverrides(CSVFile):
    """CSV overrides"""

    @staticmethod
    def _csv_overrides_line_creator(line: List[str]):
        override_data = {}
        sentence_id = line[0]

        sentence_id = int(sentence_id)
        try:
            overwritten_json_ids = [int(x) for x in line[1].split(';')]
            override_data[sentence_id] = OverridePermission(force_id=overwritten_json_ids)
        except ValueError:
            override_data[sentence_id] = OverridePermission(allow=False)
        return override_data

    def __init__(self, path: Path):
        super().__init__(
            path,
            assert_headers=["sentence_id", "overwritten_json_id"],
            line_creator=self._csv_overrides_line_creator
        )


class InsertInstructions:
    def __init__(self, after_id: int, row: Row, csv_id: int):
        self.after_id = after_id
        self.row = row
        self.csv_id = csv_id

    def raw_csv_data(self):
        return [
            self.row.from_whom,
            self.row.to_whom,
            self.csv_id,
            self.row.dialogue
        ]


class CSVInserts(CSVFile):
    """CSV inserts
    TODO: Add inserts, so we can fix up the LA Times' not included characters
    TODO: split this file into small chunks
    """

    @staticmethod
    def _csv_insert_line_creator(line: List[str]):
        override_data: Dict[int, List[InsertInstructions]] = {}
        after_id = int(line[0])
        dialogue = line[1].strip()
        from_whom = line[2].strip()
        to_whom = line[3].strip()

        override_data.setdefault(after_id, [])
        override_data[after_id].append(
            InsertInstructions(
                after_id=after_id,
                row=Row(
                    dialogue=dialogue,
                    from_whom=from_whom,
                    to_whom=to_whom,
                    id=-1
                ),
                csv_id=after_id + 1,
            )
        )

        return override_data

    def __init__(self, path: Path):
        super().__init__(
            path,
            assert_headers=["after_id", "dialogue", "from", "to"],
            line_creator=self._csv_insert_line_creator
        )


class Overrides:
    def __init__(self, dir: Path, global_override: GlobalOverride):
        self.dir = dir
        try:
            self.overrides = CSVOverrides(dir / "overrides.csv")
        except FileNotFoundError:
            self.overrides = None

        try:
            self.inserts = CSVInserts(dir / "inserts.csv")
        except FileNotFoundError:
            self.inserts = None
        self.global_override = global_override

    def should_insert(self, row: Union[JsonRow, CsvRow]) -> Optional[List[InsertInstructions]]:
        """Should I insert a new line not originally included in the dataset, after the
        given parameter?"""
        if not self.inserts:
            return None

        if isinstance(row, CsvRow):
            return self.inserts.override_data.get(row.csv_id_original)
        else:
            return None

    def give_permission(self, csv_sentence: Sentence, json_sentence: Sentence = None) -> OverridePermission:
        if csv_sentence.id_original in self.overrides.override_data:
            return self.overrides.override_data[csv_sentence.id_original]
        else:
            for regex in self.global_override.csv.regexes:
                if regex.fullmatch(csv_sentence.sentence):
                    module_logger.info(
                        f'Regex "{regex.pattern}" caught '
                        f'"{csv_sentence.sentence}" in csv (id: "{csv_sentence.id}")!'
                    )
                    return OverridePermission.Forbid
            if json_sentence:
                if len(self.global_override.json.regexes) > 0:
                    for regex in self.global_override.json.regexes:
                        if regex.fullmatch(json_sentence.sentence):
                            return OverridePermission.Forbid

            return OverridePermission.Allow

    def should_try_replace(self, csv_sentence: Sentence):
        return self.global_override.csv.should_try_replace(csv_sentence)
