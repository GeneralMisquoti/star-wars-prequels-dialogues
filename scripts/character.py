#FIXME: in current implementation this is not used
import re
from quote import Quote


class Character:
    def __init__(self, name: str):
        self.name = name
        self.quotes = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name and len(self.quotes) == len(other.quotes)

    def __repr__(self):
        return f'<Character name="{self.name}">'

    def add_quote(self, quote: re.Match):
        self.quotes.append(Quote(self, quote))
        pass

    def has_quotes(self):
        return len(self.quotes) > 0
