from .utils.row_abstract import Row


class JsonRow(Row):
    def __init__(self, json_obj: dict, id: int, index=int):
        self._json_obj = json_obj
        self.yarn_id = json_obj['id']
        self.transcript = json_obj['transcript']
        self.start_time = json_obj['start_time']
        self.end_time = json_obj['end_time']
        super().__init__(
            dialogue=self.transcript,
            id=id,
            index=index
        )
