import re

from movies import movies, Movies, NotAPrequel
from character import Character
from quote import Quote
from typing import Dict, List, Set


class CharacterManager:
    mappings = {
        'DOFINE': Character('CAPTAIN DAULTRAY DOFINE'),
        'PALPATINE': Character('SUPREME CHANCELLOR PALPATINE')
    }

    def __init__(self):

        self.characters: Set[Character] = {
            Character('SUPREME CHANCELLOR PALPATINE'),
            Character('CAPTAIN DAULTRAY DOFINE')
        }

        self.quotes: Dict[Character, List[Quote]] = dict()

    def add_character(self, character: Character):
        character = self.char_mapped(character)

        pass

    def add_quote(self, character: Character):
        character = self.char_mapped(character)

    @staticmethod
    def char_mapped(character: Character):
        for word in character.name:
            if word in CharacterManager.mappings:
                return CharacterManager.mappings[word]
        return character


class MovieData:
    def __init__(
            self,
            character_pattern: re.Pattern,
            quote_pattern: re.Pattern,
            ignored: List[str] = (),
            blacklist_substrings=('INT. ', 'EXT. ')
    ):
        self.character_pattern = character_pattern
        self.quote_pattern = quote_pattern
        self.ignored = ignored
        self.blacklist_substrings = blacklist_substrings

    def filter(self, character: Character) -> bool:
        if character.name in self.ignored:
            return False
        if any((x in character.name for x in self.blacklist_substrings)):
            return False
        return True


def parse_script(movie: MovieData, scr_text: str):
    if movie not in movies:
        raise NotAPrequel
    pass