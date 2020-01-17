from pathlib import Path
import json
import aiohttp
import asyncio

here = Path(__file__).parent
sources_dir = here.parent
added_characters_path = here / "parsed"


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
		self.mappings.setdefault(c.name, {})
		self.mappings[c.name].setdefault('in_movies', [])
		self.mappings[c.name]['in_movies'].append(c)
		self.characters_count += 1

	def __repr__(self):
		return f'<Characters len={self.characters_count}>'

	def __iter__(self):
		return self.mappings.__iter__()

	def __getitem__(self, key):
		return self.mappings[key]

	def __setitem__(self, key, value):
		self.mappings[key] = value

	def items(self):
		return self.mappings.items()


responses_path = Path(here) / "responses.json"
link_choices_path = Path(here) / "link_choices.json"
fixed_choices_path = Path(here) / "link_choices_fixed_by_hand.json"


async def get_character(session: aiohttp.ClientSession, character: str):
	url = f"https://starwars.fandom.com/api/v1/Search/List?query={character.replace(' ', '+')}&rank=most-viewed&limit=5&minArticleQuality=10&batch=1&namespaces=0"
	print(f"Getting url: \"{url}\"")
	resp = await session.get(url)
	return await resp.json(encoding="UTF-8")


async def main():
	# if not added_characters_path.exists() or not added_characters_path.is_dir():
	# 	added_characters_path.mkdir()

	files = dict()
	characters = Characters()

	for file in sources_dir.glob('*.json'):
		json_file = json.load(file.open('r', encoding='UTF-8'), encoding='UTF-8')
		files[file] = json_file

		for i, c in enumerate(json_file['characters']):
			characters.add(Character(file, c, i))

	session = None

	if not responses_path.exists() or responses_path.is_dir():
		responses = dict()
		session = aiohttp.ClientSession()
		for character in characters:
			responses[character] = get_character(session, character)

	else:
		responses = json.load(responses_path.open('r', encoding="UTF-8"))

	mappings = dict()

	fixed_choices = None
	if fixed_choices_path.exists():
		fixed_choices = json.load(fixed_choices_path.open('r', encoding="UTF-8"))

	if not link_choices_path.exists():
		items = characters.items()
		if fixed_choices:
			for name, character in items:
				if name in fixed_choices:
					character['link'] = fixed_choices[name]
					mappings[name] = fixed_choices[name]
				elif name in responses:
					character['link'] = responses[name]['items'][0]['url']
					mappings[name] = character['link']
				else:
					print(f'Getting new character "{name}"')
					if session is None:
						session = aiohttp.ClientSession()
					responses[name] = await get_character(session, name)
					character['link'] = responses[name]['items'][0]['url']
					mappings[name] = character['link']

		json.dump(mappings, link_choices_path.open('w+', encoding="UTF-8"), ensure_ascii=False)
	else:
		mappings = json.load(link_choices_path.open('r', encoding="UTF-8"))
		# mappings = dict()
		if fixed_choices:
			for mapping in fixed_choices:
				if mapping in fixed_choices:
					mappings[mapping] = fixed_choices[mapping]
			json.dump(mappings, link_choices_path.open('w', encoding="UTF-8"), ensure_ascii=False)
	if session is not None:
		await session.close()
	json.dump(responses, responses_path.open('w+', encoding="UTF-8"), ensure_ascii=False)
	print(mappings)

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

