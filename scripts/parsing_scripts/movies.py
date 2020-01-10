from enum import Enum
from typing import List, Set, Dict, Union
import re
from character import Character

names = ["phantom_menace", "attack_of_the_clones", "revenge_of_the_sith"]


class WhichMovie(Enum):
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
			character_pattern: re.Pattern = '',
			quote_pattern: re.Pattern = '',
			ignored: List[str] = (),
			blacklist_substrings=('INT. ', 'EXT. ', '- DAY', '- NIGHT'),
			mappings: Dict[str, str] = dict(),
			short_characters: Set[str] = set()
	):
		self.character_pattern = character_pattern
		self.quote_pattern = quote_pattern
		self.ignored = ignored
		self.blacklist_substrings = blacklist_substrings
		self.mappings = mappings
		self.short_characters = short_characters

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


class Movie:
	def __init__(self, name: str):
		if name not in names:
			raise NotAPrequel
		self.name: str = name
		self.which: WhichMovie = name_dict[name]
		self.data: MovieData = self.create_data()

	def assert_ready(self):
		assert self.data
		self.data.assert_ready()

	def create_data(self):
		data = MovieData()
		if self.which == WhichMovie.PHANTOM_MENACE:
			data.quote_pattern = re.compile(r'^([A-Z\-\s0-9\.]+)\s*:\s*(.*$)')
			data.character_pattern = re.compile(r'([A-Z0-9][A-Z0-9 \-\.]*[A-Z0-9])')
			data.ignored = ['TITLE CARD', 'A R', 'V.O', 'O.S', 'DROID SARGEANT', 'EXPLOSION', 'EIRTAE', 'PROTOCOL DROID',
							'SANDO AQUA MONSTER', 'JAR', 'WHEN YOUSA TINK WESA IN TROUBLE', '327 N', '523 A', '000 R',
							'BATTLE DROIDS', 'WHEEL DROIDS', 'SECOND QUEEN']
			data.mappings = {
				'DOFINE': 'CAPTAIN DAULTRAY DOFINE',
				'PALPATINE': 'SUPREME CHANCELLOR PALPATINE'
			}
			data.short_characters = {"A", "B"}
		elif self.which == WhichMovie.ATTACK_OF_THE_CLONES:
			return None
		elif self.which == WhichMovie.REVENGE_OF_THE_SITH:
			return None
		else:
			raise NotAPrequel(self.name)

		return data


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
