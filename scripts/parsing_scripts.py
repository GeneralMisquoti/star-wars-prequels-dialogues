from pathlib import Path
from bs4 import BeautifulSoup

from movies import movie_dict, name_dict, WhichMovie
from parse_script import parse_script
from save_quotes import save_quotes
from here import here

source_dir: Path = here / "scripts"

for file in source_dir.glob('*.html'):
	filename = file.stem

	movie = name_dict.get(filename, None)
	if movie is None:
		raise Exception(f'Unknown html file "{filename}" in directory (not a prequel movie).')

	file_path = source_dir / file
	with file_path.open('r', encoding="UTF-8") as html:
		parsed_html = BeautifulSoup(html.read(), features="html.parser")
		scr_text = parsed_html.find("td", attrs={'class': 'scrtext'}).text.strip()
	c, q = parse_script(filename, scr_text)
	save_quotes(movie, c, q)



