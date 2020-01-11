import re

from movies import CachedMovie, Movie
from quote import Quote, SerializeQuote
from typing import Dict, List, Union, Tuple, Optional


class CharacterManager:
	""" Manages characters ;) """
	def __init__(self, movie: Movie):
		self.movie = movie  #: xd
		""" A Movie the Manager uses to get regex data etc.  """
		self.characters: Dict[int, str] = dict()  #: xd
		""" mapping from character's index to its name """
		self.quotes: Dict[int, List[Quote]] = dict()
		""" mapping from character's index to a list of its quotes """
		self.mappings: Dict[str, int] = dict()
		""" mapping from one of character's names to its index """

	def serialized_quotes(self) -> List[SerializeQuote]:
		return [SerializeQuote(q.quote, self.mappings[q.character]) for x in self.quotes.values() for q in x]

	def __add_character(self, c: str) -> int:
		existing_character_index = self.find_character_containing_word(c)
		if existing_character_index:
			# Character exists
			existing_character = self.characters[existing_character_index]
			if len(existing_character) < len(c):
				self.replace_with_longer(c, existing_character)
				return existing_character_index
			else:
				pass

		i = len(self.characters)
		self.characters[i] = c
		self.mappings[c] = i
		self.quotes[i] = []
		return i

	def add_character(self, character: str) -> Optional[int]:
		""" :return: None if character is ignored """
		character = self.character_mapped(character)
		if character in self.mappings:
			return self.mappings[character]
		elif character is None:
			return None
		return self.__add_character(character)

	def add_quote(self, c: str, q: str, line: str):
		character = self.character_mapped(c)
		if character is None:
			return

		quote = Quote(c, q, line)
		character_index = self.mappings.get(character, None)

		if character_index is None:
			character_index = self.__add_character(character)

		self.quotes[character_index].append(quote)

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
				if quote.quote.strip() == "": continue
				found_not_empty = True
				q = SerializeQuote(quote.quote.strip(), i)
				quotes.append(q)
			if found_not_empty:
				i = len(characters)
				characters.append(self.characters[c])

		return characters, quotes


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

		if find_quote_result:
			c = find_quote_result.group(1).strip()
			q = find_quote_result.group(2).strip()
			manager.add_quote(c, q, line)

		elif find_character_result:

			# Remove characters from data.ignored
			find_character_result = map(lambda x: x.strip(), filter(movie.data.filter, find_character_result))

			for c in find_character_result:
				manager.add_character(c)

	return manager.serialize()

