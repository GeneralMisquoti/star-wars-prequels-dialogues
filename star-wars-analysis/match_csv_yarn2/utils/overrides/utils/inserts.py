from .utils.file_csv_abstract import CSVFile
from typing import Dict, List
from ...utils.row_abstract import Row
from pathlib import Path


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
    """CSV inserts"""

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
