#REWRITE THIS SHIT
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
from typing import List
from pprint import pprint
import json
from json import JSONEncoder

here = Path(__file__).parent
parsed_scripts = here / "parsed_scripts"
if not os.path.isdir(parsed_scripts) or not os.path.exists(parsed_scripts):
    os.mkdir(parsed_scripts)
source_dir: Path = here.parent


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Quote:
    paren_pattern = re.compile('\(.*\)')

    def __init__(self, char, match: re.Match):
        groups = match.groups()
        self.text = match.string
        self.quote = re.sub(self.paren_pattern, '', groups[1]).strip()
        self.character_name = groups[0].strip()
        self.character = char

    def __repr__(self):
        return f'<"{self.quote}" author="{self.character_name}">'


class SerializeQuote:
    def __init__(self, x: Quote):
        self.character = x.character_name
        self.quote = x.quote


class Character:
    def __init__(self, name: str):
        self.name = name
        self.quotes = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name and len(self.quotes) == len(other.quotes)

    def __repr__(self):
        return f'<Character name="{self.name}">'

    def add_quote(self, quote: re.Match):
        self.quotes.append(Quote(self, quote))
        pass

    def has_quotes(self):
        return len(self.quotes) > 0

#
# class SerializeCharacter:
#     def __init__(self, x: Character):
#         self = x.name


def filter_characters(characters):
    filtered = ["TITLE CARD"]

    def f(c: Character):
        return c.has_quotes() and c.name not in filtered

    return list(filter(f, characters))


def create_quotes(characters):
    quotes = []
    for c in characters:
        quotes.extend([SerializeQuote(x) for x in c.quotes])

    return quotes


def save_c_and_q(name: str, characters: List[str], quotes: List[SerializeQuote], mappings: dict):
    # new_characters = []
    characters = set(characters)
    for quote in quotes:
        if quote.character in mappings:
            if isinstance(mappings[quote.character], set):
                mappings[quote.character] = sorted(list(mappings[quote.character]), key=lambda x: len(x.quotes))[0].name
            quote.character = mappings[quote.character]
            characters.add(quote.character)
    characters = list(characters)
    for quote in quotes:
        quote.character = characters.index(quote.character)

    json.dump(
        {'characters': characters, 'quotes': quotes},
        open(parsed_scripts / (name+".json"), 'w+', encoding='UTF-8'),
        ensure_ascii=False,
        cls=MyEncoder,
        check_circular=False
    )


def parse_script_1(text: str):
    characters = {Character('A'), Character('B'), Character('SUPREME CHANCELLOR PALPATINE'), Character("CAPTAIN DAULTRAY DOFINE")}
    mappings = {
        'DOFINE': {Character('CAPTAIN DAULTRAY DOFINE')},
        'PALPATINE': {Character('SUPREME CHANCELLOR PALPATINE')}
    }
    # https://www.imsdb.com/scripts/Star-Wars-The-Phantom-Menace.html

    # character names
    # char_pattern = re.compile('([A-Z0-9]{2}[A-Z0-9\s\-\.]*[A-Z0-9])')
    char_pattern = re.compile('([A-Z0-9][A-Z0-9 \-\.]*[A-Z0-9])')
    # quotes
    quote_pattern = re.compile('^([A-Z\-\s0-9\.]+)\s*:\s*(.*$)')
    # set_mappings = {
    #     'DOFINE': Character('CAPTAIN DAULTRAY DOFINE'),
    #     'PALPATINE': Character('SUPREME CHANCELLOR PALPATINE')
    # }
    for line in text.splitlines():
        find_quote_result = re.search(quote_pattern, line)
        find_characters_result = re.findall(char_pattern, line)
        if find_characters_result:
            found_character = False
            def filter_results(x):
                return x not in ['A R', 'V.O', 'O.S', 'DROID SARGEANT', 'EXPLOSION', 'EIRTAE', 'PROTOCOL DROID', 'SANDO AQUA MONSTER', 'JAR', 'WHEN YOUSA TINK WESA IN TROUBLE', '327 N', '523 A', '000 R', 'BATTLE DROIDS', 'WHEEL DROIDS', 'SECOND QUEEN']
            find_characters_result = filter(filter_results, find_characters_result)
            for character_string in find_characters_result:
                character_string = character_string.strip()
                # ignore int ext
                if any((x in character_string for x in ['INT. ', 'EXT. '])):
                    break

                character = Character(character_string)
                # found_set_mapping = False
                # for c in set_mappings.keys():
                #     if c in character_string:
                #         mappings.setdefault(character_string, set())
                #         mappings[character_string].add(set_mappings[c])
                #         character = set_mappings[c]
                #         found_set_mapping = True
                #         break
                # if found_set_mapping:
                #     continue

                for existing_character in characters:
                    if character_string not in ["DROIDS", "GUARDS"] and character_string in existing_character.name:
                        # if new name is longer than existing
                        if len(existing_character.name) < len(character_string):
                            characters.remove(existing_character)
                            characters.add(character)
                        elif existing_character.name != character_string:
                            mappings.setdefault(character_string, set())
                            mappings[character_string].add(existing_character)

                        character = existing_character
                        characters.add(character)
                        break
                else:
                    # if hasn't broken out of loop, i.e. new character
                    characters.add(character)

            if find_quote_result and not found_character:
                speaker = find_quote_result.group(1).strip()
                if not character_string == speaker:
                    continue
                mappings[speaker]:set
                found_character = True
                character.add_quote(find_quote_result)
                # elif speaker in set_mappings and set_mappings[speaker].name == character.name:
                #     found_character = True # don't repeat, two people cant speak on same line
                #     characters.remove(set_mappings[speaker])
                #     set_mappings[speaker].add_quote(find_quote_result)
                #     characters.add(set_mappings[speaker])
                # else:
                #     if speaker in mappings:
                #         set_sp = list(mappings[speaker])[0]
                #         if set_sp.name == character.name:
                #             found_character = True
                #             if set_sp.name in [x.name for x in set_mappings.values()]:
                #                 characters.remove(set_mappings[speaker])
                #                 set_mappings[speaker].add_quote(find_quote_result)
                #                 characters.add(set_mappings[speaker])
                #             character.add_quote(find_quote_result)
                #     else:
                #         pass


    return mappings, characters

def parse_script_2(text: str):
    # https://www.imsdb.com/scripts/Star-Wars-Attack-of-the-Clones.html
    pass


def parse_script_3(text: str):
    # https://www.imsdb.com/scripts/Star-Wars-Revenge-of-the-Sith.html
    pass




for (_, _, filenames) in os.walk(source_dir):
    for file in filenames:
        file: str
        if not file.endswith(".html"):
            continue
        file_path = source_dir / file
        scr_text: str = ""
        with open(file_path, 'r', encoding="UTF-8") as html:
            parsed_html = BeautifulSoup(html.read())
            scr_text = parsed_html.find("td", attrs={'class': 'scrtext'}).text.strip()

        filename = '.'.join(file.split(".")[:-1])
        if filename == "phantom_menace":
            mappings, characters = parse_script_1(scr_text)
            characters = filter_characters(characters)
            quotes = create_quotes(characters)
            save_c_and_q("phantom_menace", [x.name for x in characters], quotes, mappings)
        elif filename == "attack_of_the_clones":
            parse_script_2(scr_text)
        elif filename == "revenge_of_the_sith":
            parse_script_3(scr_text)
        else:
            raise Exception(f"Unknown html file {filename}")


    break
