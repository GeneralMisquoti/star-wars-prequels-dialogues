from typing import List
from .utils.row_abstract import Row


class CsvRow(Row):
    def __init__(self, row: List[str], id: int, index=None):
        self.speaker = row[0]
        self.addressed = row[1]
        self.lineorder = row[2]
        self.csv_id = self.lineorder
        self.combinedline = row[3]
        self.numberofrows = row[4]
        self.wordcount = row[5]
        self.blacklisted = False
        super().__init__(
            dialogue=self.combinedline,
            id=id,
            from_whom=self.speaker,
            to_whom=self.addressed,
            index=None
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
            if sentence.forced_matched_sentences:
                if len(sentence.forced_matched_sentences) > 1:
                    yarn_match = [
                        ';'.join([str(sentence.parent_row.yarn_id) for sentence in sentence.forced_matched_sentences])
                    ]
                else:
                    forced_sentence = sentence.forced_matched_sentences[0]
                    yarn_match = [
                        forced_sentence.id
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
        headers = ["sentence_id", "csv_id", "from", "to", "dialogue", "transcript", "yarn_id"]
        for sentence in self.sentences:
            other = sentence.best_match
            yarn_match = []
            if other:
                other = other.other
                yarn_match = [other.parent_row.transcript, other.parent_row.yarn_id]
            if sentence.forced_matched_sentences:
                if len(sentence.forced_matched_sentences) > 1:
                    yarn_match = [
                        ';'.join([f"'{sentence.sentence}'" for sentence in sentence.forced_matched_sentences]),
                        ';'.join([str(sentence.parent_row.yarn_id) for sentence in sentence.forced_matched_sentences])
                    ]
                else:
                    forced_sentence = sentence.forced_matched_sentences[0]
                    yarn_match = [
                        forced_sentence.sentence,
                        forced_sentence.id
                    ]
            to_be_returned.append(
                [
                    sentence.id,
                    self.lineorder,
                    self.from_whom,
                    self.to_whom,
                    sentence.sentence,
                    *yarn_match
                ]
            )
        return headers, to_be_returned

