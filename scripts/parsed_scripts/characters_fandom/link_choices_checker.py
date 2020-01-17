import json
from characters_fandom import link_choices_path, fixed_choices_path
choices_json: dict = json.load(fixed_choices_path.open('r', encoding="UTF-8"))

def check(json_data: dict):
	keys = list(enumerate(list(json_data.keys())))
	for i, key1 in keys:
		if json_data[key1].endswith('Legends'):
			print(f'Character\'s "{key1}" url: "{json_data[key1]}" is a Legends URL!')
		for j, key2 in keys[i+1:]:
			if key1 in key2:
				print(f'"{key1}" is part of "{key2}"')
			if key2 in key1:
				print(f'"{key2}" is part of "{key1}"')


if __name__ == "__main__":
	check(choices_json)
