from typing import List
from .utils.sentence import Sentence


def split_row(row: str) -> List[str]:
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
                    if x_strip[
                        -1] in splitters:  # 'Yes, Master. How do you think this trade viceroy will deal with the chancellor\'s demands?'
                        new_split.append(x_strip)
                    else:
                        if x_strip[-1] != ',':
                            new_split.append(f'{x_strip}{splitter}')
                        else:
                            new_split.append(x_strip)
        if len(new_split) != 0:
            split = new_split
    return split


def make_sentences(row: "Row", id: int):
    return [Sentence(sentence, id + i, row) for i, sentence in enumerate(split_row(row.dialogue))]


Character = str


class Row:
    def __init__(
            self,
            dialogue: str,
            id: int,
            from_whom: Character = None,
            to_whom: Character = None,
            index: int = None,
            row_offset: int = None,
            sentence_offset: int = None
    ):
        self.dialogue = dialogue
        self.id = id
        self.original_index = index
        self.row_offset = row_offset
        self.sentence_offset = sentence_offset
        if index:
            self.index = index + self.row_offset
        else:
            self.index = index
        self.sentences = make_sentences(self, id)
        self.from_whom = from_whom
        self.to_whom = to_whom

        self.pair = None

    def __repr__(self):
        return f'<{self.__class__.__name__} from="{self.from_whom}" line="{self.sentences}" to="{self.to_whom}">'

    def __iter__(self):
        return self.sentences.__iter__()
