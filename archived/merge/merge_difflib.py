"""
1. Problem - quotes aren't the same (misspelling and such)
2. More important problem - script contains some cut scenes so stuff may get out of sync
3. Most important problem - script generally has longer strings,
4. Weird problem - yarn may have two quotes at once
Illustration: https://i.imgur.com/PqyB0aK.png

Combating 1: fuzzy search
Combating 2:
	1. buffer -> look a certain amount forward and if
		the score doesn't get better then choose max out of buffer
			I. if latter is worse than former by a scale larger
				than some constant assume first was correct (0.2?)
	2. if you find a better one *after skipping* some, then remove
		the skipped quotes assuming yarn does not have this data
Combating 3: Remove fuzzy matched yarn quotes from scripts, but
	only remove the whole script quote if len(0) of the script
Combating 4: Split yarn quote by '-' dialogue marker, and separately
	match every single dialogue line.

New problem 4->a: Now for each yarn quote you may have multiple
	subquotes and for each of them you may have a different character,
	but both script quotes must lead to the same yarn quote!

Combating 4->a: list
"""
import difflib
import json
from typing import List

from paths import here_path, top_dir
from movies import movies, WhichMovie, name_dict, movie_dict
from quote import Quote
from load_files import yarn_file_paths, parsed_scripts_file_paths, fandom_links_file_path
from difflib_match import difflib_match

merged_dir_path = here_path / "merged_difflib"
if not merged_dir_path.exists():
	merged_dir_path.mkdir()

character_links = json.load(fandom_links_file_path.open('r', encoding='UTF-8'))


class SearchedQuoteBuilder():
	def __init__(self, characters):
		self.characters = characters
		self.num_quotes = 0

	def __call__(self, q):
		self.num_quotes += 1
		return SearchedQuote(q, characters, self.num_quotes)


class SearchedQuote(Quote):
	def __init__(self, q, characters: List[str], order: int):
		character_index = q['character']
		character = characters[character_index]
		quote = q['quote']
		super().__init__(q, quote, character_index, order)
		self.len = len(quote)
		self.len_matched = 0
		self.matched: List[str] = []
		self.match_memo: List[(int, str)] = []

	def __len__(self):
		return self.len

	def set_matched(self, matched_str: str):
		self.len_matched += len(matched_str)
		self.matched.append(matched_str)
		return self.len - self.len_matched

	def memoize_match(self, match_amount: int, matched_str: str):
		self.match_memo.append((match_amount, matched_str))

	def pop_memo_match(self) -> (int, str):
		return self.match_memo.pop()


class SearchedQuoteManager:
	SEARCHED_BUFFER = 20
	ENOUGH_TO_CALL_IT_QUITS = 0.2
	def __init__(self, quotes: List[SearchedQuote]):
		self.quotes = quotes

	def match(self, yarn: str):
		prev_match_amount = 0
		prev_str = None
		for i in range(self.SEARCHED_BUFFER):
			match_amount, match = difflib_match(yarn, self.quotes[i].quote)
			self.quotes[i].memoize_match(match_amount, match)
			if i > 0:
				if match_amount < prev_match_amount + self.ENOUGH_TO_CALL_IT_QUITS:
					match_amount = prev_match_amount
					match = prev_str
					break

			prev_match_amount = match_amount
			prev_str = match
		else:
			match = self.best_buffered_match()

		amount_left = self.quotes[0].set_matched(match)
		if amount_left < 3:
			self.quotes = self.quotes[1:]

	def best_buffered_match(self):
		class Match:
			def __init__(self, match_amount: int, match_str: str, quote: SearchedQuote):
				self.match_amount = match_amount
				self.match_str = match_str
				self.quote = quote
		matches: List[Match] = []
		for i in range(self.SEARCHED_BUFFER):
			matches.append(Match(*self.quotes[i].pop_memo_match(), self.quotes[i]))

		max(matches, key=lambda x: x.match_amount)



for script_file, yarn_file in zip(parsed_scripts_file_paths, yarn_file_paths):
	assert script_file.stem == yarn_file.stem
	movie: WhichMovie = name_dict[script_file.stem]
	script = json.load(script_file.open('r', encoding="UTF-8"))
	yarn = json.load(yarn_file.open('r', encoding="UTF-8"))

	characters = script['characters']
	sq_builder = SearchedQuoteBuilder(characters)
	sq_manager = SearchedQuoteManager([sq_builder(q) for q in script['quotes'].copy()])
	yarn_quotes = ((x['transcript'], i, x['id']) for i, x in enumerate(yarn))

	for yarn_quote, i, yarn_quote_id in yarn_quotes:
		for x in yarn_quote.split('-'):
			single_quote = x.strip()
			if single_quote != "":
				sq_manager.match(yarn_quote)

		pass


