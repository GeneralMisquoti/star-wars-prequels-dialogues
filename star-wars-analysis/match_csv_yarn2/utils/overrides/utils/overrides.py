from typing import List
from pathlib import Path
from .utils.file_csv_abstract import CSVFile


class OverridePermission:
    def __init__(self, allow: bool = True, force_id: List[int] = None):
        self.allow = allow
        self.force_id = force_id
        if not allow and force_id:
            raise Exception("Can't both disallow and force a different id!")


OverridePermission.Allow = OverridePermission()
OverridePermission.Forbid = OverridePermission(allow=False)


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
