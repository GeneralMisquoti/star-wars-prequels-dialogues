from pathlib import Path
from typing import Dict, List, Callable, Any
from csv import reader
from .. import overrides


class CSVFile:
    def headers_same(self, assert_headers, headers):
        for (ah, actual) in zip(assert_headers,headers):
            assert ah == actual.strip()

    def __init__(self, path: Path, assert_headers: List[str], line_creator: Callable[[List[str]], Dict[int, Any]]):
        self.path = path
        self.io = path.open('r', encoding='UTF-8')
        self.csv = reader(self.io)
        headers = self.csv.__next__()
        self.headers_same(assert_headers, headers)
        self.override_data: Dict[int, "overrides.OverridePermission"] = {}
        for line in self.csv:
            if len(line) == 0:
                continue
            if line[0][0] == "#":
                # Comments
                continue
            rv = line_creator(line)
            self.override_data = {**self.override_data, **rv}

        self.io.close()
