import re
from typing import List


class Quote:
	# Used to remove annotation for actors
	# and descriptions from inside dialogue lines

	def __init__(self, character: str, quote: str, id_: int):
		self.quote = quote
		self.character = character
		self.id = id_

	def __repr__(self):
		return f'<{self.character}: {self.quote if len(self.quote) < 40 else f"{self.quote[:40]}..."}>'


class QuoteCleanPattern:
	def __init__(self, quote_clean_pattern: re.Pattern, replace_with: str):
		self.quote_clean_pattern = quote_clean_pattern
		self.replace_with = replace_with

	def sub(self, q: str):
		return re.sub(self.quote_clean_pattern, self.replace_with, q)


class QuoteBuilder:
	def __init__(self, quote_clean_pattern: List[QuoteCleanPattern]):
		self.quote_clean_patterns = quote_clean_pattern

	def __call__(self, c: str, q: str, id_: int) -> Quote:
		c = c.strip()
		for clean_pattern in self.quote_clean_patterns:
			q = clean_pattern.sub(q)
		q = q.strip()

		return Quote(c, q, id_)


class SerializeQuote:
	def __init__(self, q: str, c: int):
		self.__repr__ = Quote.__repr__
		self.character = c
		self.quote = q

	@classmethod
	def from_quote(cls, q: Quote):
		cls.__repr__ = Quote.__repr__
		return cls(q.quote, q.id)
