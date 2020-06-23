from pathlib import Path
import re
from typing import Dict, List
from csv import reader
from .utils.utils.sentence import Sentence
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
    def __init__(self, blacklist_regexes=None):
        if blacklist_regexes is None:
            blacklist_regexes = []
        self.regexes = [re.compile(regex) for regex in blacklist_regexes]


class GlobalOverride:
    def __init__(self, path: Path):
        parsed_toml = toml.load(path.open('r', encoding='UTF-8'))
        self.csv = GlobalOverrideForFile(**parsed_toml.get('csv'))
        self.json = GlobalOverrideForFile(**parsed_toml.get('json'))


class Overrides:
    def __init__(self, path: Path, global_override: GlobalOverride):
        self.path = path
        self.csv = reader(path.open('r', encoding='UTF-8'))
        self.global_override = global_override
        # Make sure format is right
        headers = self.csv.__next__()
        assert ["sentence_id", "overwritten_json_id"], headers
        self.override_data: Dict[int, OverridePermission] = {}
        for line in self.csv:
            if len(line) == 0:
                continue
            sentence_id = line[0]

            # Comments
            if sentence_id[0] == "#":
                continue

            sentence_id = int(sentence_id)
            try:
                overwritten_json_ids = [int(x) for x in line[1].split(';')]
                self.override_data[sentence_id] = OverridePermission(force_id=overwritten_json_ids)
            except ValueError:
                self.override_data[sentence_id] = OverridePermission(allow=False)

    def give_permission(self, csv_sentence: Sentence, json_sentence: Sentence = None) -> OverridePermission:
        if csv_sentence.id in self.override_data:
            return self.override_data[csv_sentence.id]
        else:
            for regex in self.global_override.csv.regexes:
                if regex.fullmatch(csv_sentence.sentence):
                    module_logger.info(
                        f'Regex "{regex.pattern}" caught "{csv_sentence.sentence}" in csv (id: "{csv_sentence.id}")!')
                    return OverridePermission.Forbid
            if json_sentence:
                if len(self.global_override.json.regexes) > 0:
                    for regex in self.global_override.json.regexes:
                        if regex.fullmatch(json_sentence.sentence):
                            return OverridePermission.Forbid

            return OverridePermission.Allow
