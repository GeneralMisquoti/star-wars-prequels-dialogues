from pathlib import Path
from typing import Dict, List, Optional,  Union
from ..row_csv import CsvRow
from ..row_json import JsonRow
from ..utils.utils.sentence import Sentence
import logging

from .utils.global_overrides import GlobalOverride
from .utils.overrides import CSVOverrides, OverridePermission
from .utils.inserts import CSVInserts, InsertInstructions

module_logger = logging.getLogger(__name__)


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
