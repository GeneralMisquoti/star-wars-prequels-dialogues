import re

from movies import CachedMovie, Movie, WhichMovie
from quote import Quote, SerializeQuote, QuoteBuilder
from typing import Dict, List, Union, Tuple, Optional


class CharacterManager:
	""" Manages characters ;) """
	numerals = [
			"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
			"ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"
	]

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

	def __add_character(self, character: str, speaking=True) -> int:
		existing_character_index = self.find_character_containing_word(character)
		if existing_character_index == -1:
			# Name ends in number so even though a shorter character
			# name may fit inside it it should be treated as a different character.
			# So add it.
			pass
		elif existing_character_index is not None:
			# Character exists
			existing_character = self.characters[existing_character_index]
			if len(existing_character) < len(character):
				self.replace_with_longer(character, existing_character)
				return existing_character_index
			else:
				return existing_character_index
		else:
			# Character containing this word not found, but what if the
			# character itself is a larger string that could potentially
			# contain a substring of an existing character; therefore adding
			# more information?

			# - Ok, but what when "AT-ST CLONE SERGEANT" is someone else than "CLONE SERGEANT"?
			# - Well then if that character is speaking then add it as stand-alone character ;)
			if not speaking:
				# - Well but what if it's not speaking and still overwrites...
				# - Fuck you eat sheeit
				for i, c in self.characters.items():
					# - Oh so I'll add another data parameter for this then...
					# - Sure, why not go ahead
					if c not in self.movie.data.strict:
						# - But then why does a ..."DROID" match a ..."DROIDS"
						# - Why don't you go f...
						c_split = c.split(" ")
						character_split = character.split(" ")
						if all((c_ in character_split for c_ in c_split)):
							# - But this still does not work
							# - Well you have to update `self.find_character_containing_word`
							self.characters[i] = character
							return i

		if speaking:
			i = len(self.characters)
			self.characters[i] = character
			self.mappings[character] = i
			self.quotes[i] = []
			return i
		else:
			return -1

	def add_character(self, character: str, speaking=True) -> Optional[int]:
		"""
		:param character: name
		:param speaking: whether found in quote or stand-alone
		:return: None if character is ignored
		"""
		character = self.character_mapped(character)
		if character is None:
			return None
		if character in self.mappings:
			return self.mappings[character]

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
		if character in self.movie.data.strict:
			return None
		if character.split(" ")[-1] in self.numerals:
			return -1
		for i in self.characters:
			c = self.characters[i]
			c_split = c.split(" ")
			if character in c:
				if c_split[-1] in self.numerals:
					return -1
				return i
			for word in c_split:
				if word == character:
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
		if any((x in character for x in self.movie.data.blacklist_substrings)):
			return None
		character = character.strip()
		split_character = character.split(" ")
		if split_character[-1] not in self.numerals:
			for word in split_character:
				if word in self.movie.data.mappings:
					return self.movie.data.mappings[word]
		for name in self.movie.data.mappings:
			if name == character:
				return self.movie.data.mappings[name]
		else:
			if character in self.mappings:
				return self.characters[self.mappings[character]]

		return character

	def serialize(self, which=WhichMovie.NA):
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

				if len(quote.quote) < 4:
					print(f'Suspiciously short quote: "{quote}"')
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

	return manager.serialize(which=movie.which)
