import os
from pathlib import Path
from bs4 import BeautifulSoup
from json import JSONEncoder

from movies import movie_dict, name_dict, WhichMovie
from parse_script import parse_script
from save_quotes import save_quotes


here = Path(__file__).parent
parsed_scripts = here / "parsed_scripts"
if not os.path.isdir(parsed_scripts) or not os.path.exists(parsed_scripts):
	os.mkdir(parsed_scripts)
source_dir: Path = here.parent


class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__


for file in source_dir.glob('*.html'):
	if not file.suffix == ".html":
		continue
	filename = file.stem

	#TODO: add more movies
	if movie_dict[WhichMovie.PHANTOM_MENACE] != filename:
		continue
	movie = name_dict.get(filename, None)
	if movie is None:
		raise Exception(f'Unknown html file "{filename}" in directory (not a prequel movie).')

	file_path = source_dir / file
	with file_path.open('r', encoding="UTF-8") as html:
		parsed_html = BeautifulSoup(html.read())
		scr_text = parsed_html.find("td", attrs={'class': 'scrtext'}).text.strip()

	save_quotes(movie, *parse_script(filename, scr_text))



