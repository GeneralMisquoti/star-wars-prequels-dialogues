from pathlib import Path
import re
from typing import Optional
from ...utils.utils.sentence import Sentence
import toml


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
