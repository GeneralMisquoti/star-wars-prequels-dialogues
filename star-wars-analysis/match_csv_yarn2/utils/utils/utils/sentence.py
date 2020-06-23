from fuzzywuzzy import fuzz
import heapq
from typing import Optional, Tuple, List


class Match:
    def __init__(self, me: "Sentence", other: "Sentence", ratio: int):
        self.other = other
        self.ratio = ratio
        self.distance = abs(me.id - other.id)
        self.score = ratio - self.distance
        self.ideal_match = ratio == 100
        self.wont_be_better = False

    def __lt__(self, other):
        return self.ratio < other.ratio

    def __repr__(self):
        return f'<Match id="{self.other.id}" ratio="{self.ratio}" "{self.other.sentence}">'


class Sentence:
    def __init__(self, sentence: str, id: int, parent: "Row"):
        self.sentence = sentence
        self.id = id
        self.matches: List[Tuple[int, Match]] = []
        self.THRESHOLD_CHECK_MORE_FOR_FUN = 5

        self.best_match: Optional[Match] = None
        self.parent_row = parent
        self.forced_matched_sentences = None

    def force_matches(self, forced_sentences: List["Sentence"]):
        self.forced_matched_sentences = forced_sentences

    def match(self, other_sentence: "Sentence"):
        # https://www.datacamp.com/community/tutorials/fuzzy-string-python
        match_ratio = fuzz.partial_ratio(self.sentence, other_sentence.sentence)
        new_match = Match(
            self,
            other_sentence,
            match_ratio,
        )
        if len(self.matches) > 0:
            best_match = self.matches[0][1]
            # If next match worse than previous don't try to match all after it
            if new_match.ratio < 20 and best_match.ratio > new_match.ratio:
                best_match.wont_be_better = True
                return best_match
        heapq.heappush(self.matches, (-1 * new_match.score, new_match))
        self.best_match: Match = self.matches[0][1]
        return new_match

    def decide_on_match(self) -> Optional[Match]:
        if len(self.matches) == 0:
            return None
        self.best_match: Match = self.matches[0][1]
        if len(self.matches) > 1:
            second_best = self.matches[1][1]
            # If both are pretty good and second is right after the first then choose the second best
            # Because it's likely a word has repeated
            if self.best_match.ratio > 95 and \
               second_best.ratio > 95 and \
               second_best.other.id + 1 == self.best_match.other.id:
                return second_best
        return self.best_match

    def __repr__(self):
        return f'<Sentence id="{self.id}" "{self.sentence}">'
