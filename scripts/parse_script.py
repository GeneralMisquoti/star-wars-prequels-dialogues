import re

from movies import CachedMovie, Movie
from quote import Quote, SerializeQuote, QuoteBuilder
from typing import Dict, List, Union, Tuple, Optional


class CharacterManager:
	""" Manages characters ;) """

	def __init__(self, movie: Movie):
		self.movie = movie  #: xd
		""" A Movie the Manager uses to get regex data etc.  """
		self.characters: Dict[int, str] = dict()  #: xd
		""" Mapping from character's index to its name. """
		self.quotes: Dict[int, List[Quote]] = dict()
		""" Mapping from character's index to a list of its quo.tes """
		self.mappings: Dict[str, int] = dict()
		""" Mapping from one of character's names to its index. """
		self.quotes_count = 0
		""" Used to sort quotes later by order. """
		self.quote_builder = QuoteBuilder(self.movie.data.quote_clean_patterns)
		""" A cached object with specified regex deletion/clean patterns. """

	def serialized_quotes(self) -> List[SerializeQuote]:
		return [
			SerializeQuote(q.quote, self.mappings[q.character])
			for x in self.quotes.values()
			for q in x
		]

	def __add_character(self, c: str, speaking=True) -> int:
		existing_character_index = self.find_character_containing_word(c)
		if existing_character_index:
			# Character exists
			existing_character = self.characters[existing_character_index]
			if len(existing_character) < len(c):
				self.replace_with_longer(c, existing_character)
				return existing_character_index
			else:
				pass

		if speaking:
			i = len(self.characters)
			self.characters[i] = c
			self.mappings[c] = i
			self.quotes[i] = []
			return i
		else:
			return -1

	def add_character(self, character: str, speaking=True) -> Optional[int]:
		""" :return: None if character is ignored """
		character = self.character_mapped(character)
		if character in self.mappings:
			return self.mappings[character]
		elif character is None:
			return None
		return self.__add_character(character, speaking=speaking)

	def add_quote(self, c: str, q: str):
		character = self.character_mapped(c)
		if character is None:
			return

		quote = self.quote_builder(c, q, self.quotes_count)
		character_index = self.mappings.get(character, None)

		if character_index is None:
			character_index = self.__add_character(character)

		self.quotes[character_index].append(quote)
		self.quotes_count += 1

	def find_character_containing_word(self, character: str) -> Union[None, int]:
		"""
		:param character: Returns index of character whose one of
			the words in its names is equal to it
		"""
		for i in self.characters:
			c = self.characters[i]
			if character in c and len(character) > 3:  # len for "A", "B" characters
				return i
			for word in c.split(" "):
				if word == character and len(word) > 3:
					return i
		else:
			return None

	def replace_with_longer(self, new: str, old: str):
		index = self.mappings[old]
		self.mappings[new] = index
		self.characters[index] = new

	def character_mapped(self, character: str) -> Optional[str]:
		"""
		:param character: character to map
		:return: None if in ignored else str
		"""
		if character in self.movie.data.ignored:
			return None
		character = character.strip()
		for word in character.split(" "):
			if word in self.movie.data.mappings:
				return self.movie.data.mappings[word]
		else:
			if character in self.mappings:
				return self.characters[self.mappings[character]]
			else:
				existing_characters_index = self.find_character_containing_word(character)
				if existing_characters_index is not None:
					return self.characters[existing_characters_index]
				else:
					return character

	def serialize(self):
		"""
		We don't want characters who don't speak.
		We can't just delete them, since we depend on the indexing.

		Therefore we create a new list of characters, by looping through the
		quotes, therefore only characters who have spoken will be taken into account.
		"""
		characters = []
		quotes = []
		for c in self.quotes:
			found_not_empty = False
			i = len(characters)
			for quote in self.quotes[c]:
				if quote.quote.strip() in ["", "-"]:
					continue
				found_not_empty = True
				quote.id = i
				quotes.append(quote)
			if found_not_empty:
				i = len(characters)
				characters.append(self.characters[c])

		quotes = sorted(quotes, key=lambda q: q.id)
		quotes = list(map(SerializeQuote.from_quote, quotes))

		return characters, quotes


def parse_script(movie: str, scr_text: str) -> Tuple[List[str], List[SerializeQuote]]:
	movie = CachedMovie(movie)
	manager = CharacterManager(movie)

	find_quote_results = re.findall(movie.data.quote_pattern, scr_text)

	find_character_results = set(re.findall(movie.data.character_pattern, scr_text))
	find_character_results = list(map(lambda x: x.strip(), filter(movie.data.filter, find_character_results)))

	for quote in find_quote_results:
		c: str = quote[0].strip()
		q: str = quote[1].strip()
		manager.add_quote(c, q)

	for character in find_character_results:
		character: str
		manager.add_character(character, speaking=False)

	return manager.serialize()
