import re


class Quote:
    paren_pattern = re.compile('\(.*\)')

    def __init__(self, char, match: re.Match):
        groups = match.groups()
        self.text = match.string
        self.quote = re.sub(self.paren_pattern, '', groups[1]).strip()
        self.character_name = groups[0].strip()
        self.character = char

    def __repr__(self):
        return f'<"{self.quote}" author="{self.character_name}">'


class SerializeQuote:
    def __init__(self, x: Quote):
        self.character = x.character_name
        self.quote = x.quote
