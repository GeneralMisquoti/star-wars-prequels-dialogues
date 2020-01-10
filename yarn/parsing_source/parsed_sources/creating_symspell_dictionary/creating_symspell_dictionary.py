import os
from pathlib import Path
from typing import List
import json

here = Path(__file__).parent
created_dict = here / "created_dict"
if not os.path.isdir(created_dict) or not os.path.exists(created_dict):
	os.mkdir(created_dict)
parsed_dir: Path = here.parent


def parse_json(file_path: Path):
	assert file_path.parent == parsed_dir
	json_data = json.load(open(file_path, 'r', encoding="UTF-8"))
	return json_data


datas = []

for (_, _, filenames) in os.walk(parsed_dir):
	for file in filenames:
		file: str
		if not file.endswith(".json"): continue
		if file == "videos.json": continue
		file_path = parsed_dir / file
		movie_data = parse_json(file_path)
		datas.extend(movie_data)
	break

def get_movie_id(id: int) -> int:
	return id - 187245 + 1
	
filename = 'dict.txt'
with open(created_dict / filename, 'w+', encoding="UTF-8") as f:
	for line in datas:
		if not isinstance(line, dict):
			print(f"Line is not dict, but {type(line)} instead: ", line)
			continue
		line_text: str = line['transcript']
		line_text = line_text.lower()
		num_words = len(line_text.split(" "))
		movie_id = get_movie_id(line['Video'])
		if num_words < 4:
			continue
		f.write(f"{movie_id}{line['id']};;{line_text};;1\n")
