from typing import List
from .utils.row_abstract import Row


class CsvRow(Row):
    def __init__(
            self,
            row: List[str],
            id: int,
            index: int = None,
            row_offset: int = None,
            sentence_offset: int = None,
            offset=False
    ):
        self.speaker = row[0]
        self.addressed = row[1]
        self.lineorder = row[2]
        self.csv_id_original = int(self.lineorder)
        self.csv_id_offset = self.csv_id_original + row_offset
        self.offset = offset
        if offset:
            self.csv_id_original = None
        self.combinedline = row[3]
        # self.numberofrows = row[4]
        # self.wordcount = row[5]
        self.blacklisted = False
        super().__init__(
            dialogue=self.combinedline,
            id=id,
            from_whom=self.speaker,
            to_whom=self.addressed,
            index=None,
            row_offset=row_offset,
            sentence_offset=sentence_offset
        )

    def to_map_prod(self):
        to_be_returned = []
        headers = ["from", "to", "dialogue", "yarn_id"]
        for sentence in self.sentences:
            other = sentence.best_match
            yarn_match = []
            if other:
                other = other.other
                yarn_match = [other.parent_row.yarn_id]
            if sentence.forced_matched_rows:
                if len(sentence.forced_matched_rows) > 1:
                    yarn_match = [
                        ';'.join([str(row.yarn_id) for row in sentence.forced_matched_rows])
                    ]
                else:
                    forced_row = sentence.forced_matched_rows[0]
                    yarn_match = [
                        forced_row.yarn_id
                    ]
            to_be_returned.append(
                [
                    self.from_whom,
                    self.to_whom,
                    sentence.sentence,
                    *yarn_match
                ]
            )
        return headers, to_be_returned

    def to_map_test(self):
        to_be_returned = []
        headers = ["sentence_id", "sentence_id_original", "csv_id", "from", "to", "dialogue", "transcript", "yarn_id"]
        for sentence in self.sentences:
            other = sentence.best_match
            yarn_match = []
            if other:
                other = other.other
                yarn_match = [other.parent_row.transcript, other.parent_row.yarn_id]
            if sentence.forced_matched_rows:
                if len(sentence.forced_matched_rows) > 1:
                    yarn_match = [
                        ';'.join([f"'{row.dialogue}'" for row in sentence.forced_matched_rows]),
                        ';'.join([str(row.yarn_id) for row in sentence.forced_matched_rows])
                    ]
                else:
                    forced_row = sentence.forced_matched_rows[0]
                    yarn_match = [
                        forced_row.dialogue,
                        forced_row.yarn_id
                    ]
            to_be_returned.append(
                [
                    sentence.id,
                    sentence.id_original,
                    self.lineorder,
                    self.from_whom,
                    self.to_whom,
                    sentence.sentence,
                    *yarn_match
                ]
            )
        return headers, to_be_returned
