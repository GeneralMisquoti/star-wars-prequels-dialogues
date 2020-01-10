import re


class Quote:
	# Used to remove annotation for actors
	# and descriptions from inside dialogue lines
	paren_pattern = re.compile(r'\(.*\)')

	def __init__(self, character: str, quote: str, text: str ):
		self.quote = re.sub(self.paren_pattern, '', quote).strip()
		self.character = character
		self.text = text

	@classmethod
	def from_match(cls, match: re.Match):
		groups = match.groups()
		text: str = match.string
		quote: str = re.sub(cls.paren_pattern, '', groups[1]).strip()
		character: str = groups[0].strip()
		return cls(text, quote, character)

	def __repr__(self):
		return f'<"{self.quote}" author="{self.character}">'


class SerializeQuote:
	def __init__(self, q: str, character_index):
		self.character = character_index
		self.quote = q
