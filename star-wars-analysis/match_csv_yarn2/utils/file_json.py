from .utils.file_abstract import File
from pathlib import Path
import json
from .row_json import JsonRow


class JsonFile(File):
    def __init__(self, path: Path, movie_index: int):
        super().__init__(path, movie_index)
        with path.open('r', encoding='UTF-8') as file:
            parsed_json = json.load(file)
        super().parse(parsed_json, JsonRow)
