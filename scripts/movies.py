from enum import Enum
from typing import List, Set, Dict, Union
import re
import movie_data

from character import Character
from quote import QuoteCleanPattern

names = ["phantom_menace", "attack_of_the_clones", "revenge_of_the_sith"]


class WhichMovie(Enum):
	NA = -1
	PHANTOM_MENACE = 0
	ATTACK_OF_THE_CLONES = 1
	REVENGE_OF_THE_SITH = 2


movie_dict = {
	WhichMovie.PHANTOM_MENACE: "phantom_menace",
	WhichMovie.ATTACK_OF_THE_CLONES: "attack_of_the_clones",
	WhichMovie.REVENGE_OF_THE_SITH: "revenge_of_the_sith"
}

name_dict = {
	"phantom_menace": WhichMovie.PHANTOM_MENACE,
	"attack_of_the_clones": WhichMovie.ATTACK_OF_THE_CLONES,
	"revenge_of_the_sith": WhichMovie.REVENGE_OF_THE_SITH
}


class NotAPrequel(Exception):
	def __init__(self, movie: str):
		super().__init__(f'"{movie}" is not a proper Prequel movie format')


class MovieData:
	"""
	Regex patterns are based on line per line basis.

	:param character_pattern: regex Pattern that will find every character in script regardless if on that particular
		line they are currently speaking.
		This data is stored to make sure you get the longest possible name later, which is implemented in parse_script.

	:param quote_pattern: regex Pattern that will find in *first group*: character; *second group*: actual quote

	:param blacklist_substrings: blocked substrings in characters, such as script place description, i.e. 'INT.' etc.

	:param ignored: uppercase words that are not actually characters, or characters that you are sure dont speak

	:param mappings: these are *words* that may be exactly equal to another word in a longer character name
		that all map to the same character,
		the goal is to use the most information possible for the character name and unify all those different script
		characters into a single character with that name w/e it is set to

	:param short_characters: are characters that names' could be a substring of other names
		and yet still be a distinct character
	"""

	def __init__(
			self,
			character_pattern: re.Pattern,
			quote_pattern: re.Pattern,
			ignored: List[str],
			blacklist_substrings,
			mappings: Dict[str, str] = dict(),
			short_characters: Set[str] = set(),
			quote_clean_patterns: List[QuoteCleanPattern] = [],
			which=WhichMovie.NA
	):
		self.character_pattern = character_pattern
		self.quote_pattern = quote_pattern
		self.ignored = ignored
		self.blacklist_substrings = blacklist_substrings
		self.mappings = mappings
		self.short_characters = short_characters
		self.which = which
		self.quote_clean_patterns = quote_clean_patterns

	def filter(self, character: Union[Character, str]) -> bool:
		if isinstance(character, Character):
			character = character.name
		elif not isinstance(character, str):
			raise Exception("Invalid type")

		if character in self.ignored:
			return False
		if any((x in character for x in self.blacklist_substrings)):
			return False
		return True

	def assert_ready(self):
		assert self.character_pattern != ""
		assert self.quote_pattern != ""
		assert self.ignored != ()

	def __repr__(self):
		return f'<MovieData for="{self.which}">'


def load_data(which: WhichMovie) -> MovieData:
	try:
		movie = [movie_data.phantom_menace, movie_data.attack_of_the_clones, movie_data.revenge_of_the_sith][
			which.value]
	except IndexError as e:
		raise NotAPrequel(str(e))
	data = MovieData(
		movie.character_pattern,
		movie.quote_pattern,
		ignored=movie.ignored,
		blacklist_substrings=movie.blacklist,
		mappings=movie.mappings,
		which=which,
		quote_clean_patterns=movie.quote_clean_patterns
	)

	return data


class Movie:
	def __init__(self, name: str):
		if name not in names:
			raise NotAPrequel
		self.name: str = name
		self.which: WhichMovie = name_dict[name]
		self.data: MovieData = load_data(self.which)

	def assert_ready(self):
		assert self.data
		self.data.assert_ready()

	def __repr__(self):
		return f'<Movie "{self.name}">'


class Movies:
	def __init__(self, names: List[str]):
		self.movies = []
		for name in names:
			if name not in names:
				raise NotAPrequel(name)
			self.movies.append(Movie(name))

	def __iter__(self):
		return self.movies

	def __contains__(self, item: str):
		return item in names

	def __repr__(self):
		return f'<Movies num={len(self.movies)}>'


movies = Movies(names)


class CachedMovie(Movie):
	def __call__(self, name: str):
		for movie in movies:
			if movie.name == name:
				movie.assert_ready()
				return movie
		else:
			raise NotAPrequel(name)

		pass
