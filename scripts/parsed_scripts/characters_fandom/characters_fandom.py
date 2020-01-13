from pathlib import Path
import json
# import aiohttp

here = Path(__file__).parent
sources_dir = here.parent
added_characters_path = here / "parsed"

if not added_characters_path.exists() or not added_characters_path.is_dir():
	added_characters_path.mkdir()

files = dict()


class Character:
	def __init__(self, file: Path, name: str, index: int):
		self.file = file
		self.name = name
		self.index = index

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		return self.file == other.file and self.name == other.name and self.index == other.index

	def __repr__(self):
		return f'<Character name="{self.name}" index={self.index} file="{self.file.stem}">'


class Characters:
	def __init__(self):
		self.mappings = dict()
		self.characters_count = 0

	def add(self, c: Character):
		self.mappings.setdefault(c.name, [])
		self.mappings[c.name].append(c)
		self.characters_count += 1

	def __repr__(self):
		return f'<Characters len={self.characters_count}>'


characters = Characters()

for file in sources_dir.glob('*.json'):
	json_file = json.load(file.open('r', encoding='UTF-8'), encoding='UTF-8')
	files[file] = json_file

	for i, c in enumerate(json_file['characters']):
		characters.add(Character(file, c, i))

print(characters)
