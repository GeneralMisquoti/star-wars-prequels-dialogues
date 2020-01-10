import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
from typing import List
from pprint import pprint
import json
from json import JSONEncoder

from character import Character
from quote import Quote, SerializeQuote
from movies import Movies
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
        save_quotes(parse_script(filename, scr_text))

    break


