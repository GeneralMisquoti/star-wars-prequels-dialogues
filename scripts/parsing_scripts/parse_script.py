import re

from movies import CachedMovie, Movie
from quote import Quote, SerializeQuote
from typing import Dict, List, Union, Iterable, Tuple


class CharacterManager:
	def __init__(self, movie: Movie):
		self.movie = movie
		self.characters: List[str] = []
		self.quotes: Dict[int, List[Quote]] = dict()
		self.mappings: Dict[str, int] = dict()

		for c in self.movie.data.mappings:
			self.__add_character(c)

	def serialized_quotes(self) -> List[SerializeQuote]:
		return [SerializeQuote(q.quote, self.mappings[q.character]) for x in self.quotes.values() for q in x]

	def __add_character(self, c):
		self.characters.append(c)
		i = len(self.characters) - 1
		self.mappings[c] = i
		return i

	def add_character(self, character: str):
		character = self.character_mapped(character)
		existing_character = self.find_longer_character(character)
		if existing_character and len(existing_character) < len(character):
			self.replace_with_longer(character, existing_character)
		else:
			if character not in self.mappings:
				self.__add_character(character)

		return character

	def add_quote(self, c: str, q: str, line: str):
		character = self.character_mapped(c)
		quote = Quote(c, q, line)
		character_index = self.mappings.get(character, None)

		if character_index is None:
			character_index = self.__add_character(c)

		if character_index not in self.quotes:
			self.quotes[character_index] = []
		self.quotes[character_index].append(quote)

	def find_longer_character(self, character: str) -> Union[None, str]:
		for c in self.characters:
			for word in c.split(" "):
				if word == character:
					return c
		else:
			return None

	def replace_with_longer(self, new: str, old: str):
		index = self.mappings[old]
		self.mappings[new] = index
		self.characters[index] = new

	def character_mapped(self, character: str):
		for word in character:
			if word in self.movie.data.mappings:
				return self.movie.data.mappings[word]
		return character


def parse_script(movie: str, scr_text: str) -> Tuple[List[str], List[SerializeQuote]]:
	movie = CachedMovie(movie)
	manager = CharacterManager(movie)

	# Loop through every line in script
	for line in (x for x in scr_text.splitlines() if x != ''):
		# This assumes only one quote per line!
		find_quote_result = re.search(movie.data.quote_pattern, line)

		# Findall (instead of search) because there may be
		# more than one character on a single line
		find_character_result = re.findall(movie.data.character_pattern, line)

		if find_character_result:

			# Remove characters from data.ignored
			find_character_result = map(lambda x: x.strip(), filter(movie.data.filter, find_character_result))

			for c in find_character_result:
				manager.add_character(c)

		if find_quote_result:
			c = find_quote_result.group(1).strip()
			q = find_quote_result.group(2).strip()
			manager.add_quote(c, q, line)

	return manager.characters, manager.serialized_quotes()

