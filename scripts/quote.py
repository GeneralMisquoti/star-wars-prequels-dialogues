import re
from typing import List


class Quote:
	# Used to remove annotation for actors
	# and descriptions from inside dialogue lines

	def __init__(self, character: str, quote: str, character_index: int, order: int):
		self.quote = quote
		self.character = character
		self.character_index = character_index
		self.order = order

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

	def __call__(self, c: str, q: str, character_index: int, order:int) -> Quote:
		c = c.strip()
		for clean_pattern in self.quote_clean_patterns:
			q = clean_pattern.sub(q)
		q = q.strip()

		return Quote(c, q, character_index, order)


class SerializeQuote:
	def __init__(self, q: str, c_i: int):
		self.__repr__ = Quote.__repr__
		self.character = c_i
		self.quote = q

	@classmethod
	def from_quote(cls, q: Quote):
		cls.__repr__ = Quote.__repr__
		return cls(q.quote, q.character_index)
