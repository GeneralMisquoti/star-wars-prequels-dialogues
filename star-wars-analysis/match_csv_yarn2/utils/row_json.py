from .utils.row_abstract import Row


class JsonRow(Row):
    def __init__(self, json_obj: dict, id: int):
        self._json_obj = json_obj
        self.yarn_id = json_obj['id']
        self.transcript = json_obj['transcript']
        super().__init__(
            dialogue=self.transcript,
            id=id
        )
