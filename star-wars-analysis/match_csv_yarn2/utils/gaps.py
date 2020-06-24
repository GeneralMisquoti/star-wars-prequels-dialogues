from typing import List, Tuple
from pathlib import Path
from .utils.utils.sentence import Match, Sentence
from .utils.row_abstract import Row
from .utils.file_abstract import Movie
import logging
from datetime import timedelta

# https://stackoverflow.com/questions/8906926/formatting-timedelta-objects
from string import Template


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


class Gap:
    def __init__(self, yarn_ids: Tuple[int, int], row_indexes: Tuple[int, int]):
        self.yarn_ids = yarn_ids
        self.row_indexes = row_indexes


class DetectGaps:
    def __init__(self, log_path: Path, movie: Movie):
        self.path = log_path
        self.logger = logging.getLogger("gaps_" + movie.name)
        self.logger.propagate = False
        self.log_handler = logging.FileHandler(
            self.path,
        )
        self.log_handler.setFormatter(
            logging.Formatter("%(message)s")
        )
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.DEBUG)
        self._log(f'Starting gap detection on movie "{movie.name}"')

        self.movie = movie
        self.gap_count = 0
        self.all_count = 0

        self.prev_match = None
        self.prev_sentence = None

    def take_note_of_forced_rows(self, csv_sentence: Sentence):
        self.prev_sentence = csv_sentence
        json_sentence = csv_sentence.forced_matched_rows[-1].sentences[-1]
        self.prev_match = Match(csv_sentence, json_sentence, 100)

    def detect(self, match: Match, sentence: Sentence, movie_index: int = -1) -> Gap:
        """
        :param match: match.other JSON
        :param sentence: CSV
        """
        found_gap = None
        if self.prev_match:
            prev_row = self.prev_match.other.parent_row
            prev_id: int = prev_row.yarn_id

            cur_row = match.other.parent_row
            cur_id: int = cur_row.yarn_id
            if cur_id > prev_id and prev_id + 1 != cur_id:
                start: int = prev_row.index + 1
                end: int = cur_row.index
                start_time = timedelta(seconds=self.prev_match.other.parent_row.end_time)
                end_time = timedelta(seconds=match.other.parent_row.start_time)
                tmplt = '%H:%M:%S'
                start_time = strfdelta(start_time, tmplt)
                end_time = strfdelta(end_time, tmplt)

                self._log(
                    f"Missed {end - start} sentences between "
                    f"csv_id[{self.prev_sentence.parent_row.csv_id_original}:{sentence.parent_row.csv_id_original}]: "
                    f"{[x.yarn_id for x in self.movie.rows[start:end]]}."
                    f"From {start_time} to {end_time}."
                )
                for missed_row in self.movie.rows[start:end]:
                    self._log_gap(missed_row.sentences)

                found_gap = Gap(
                    yarn_ids=(prev_id, cur_id),
                    row_indexes=(start, end)
                )

        self.prev_match = match
        self.prev_sentence = sentence
        self.all_count += 1
        return found_gap

    def _log_gap(self, missed_sentence: Row):
        self.gap_count += 1
        self._log(f"GAP: {str(missed_sentence)}")

    def _log(self, text: str):
        self.logger.info(text)

    def log_count(self):
        self._log(f"In total {self.gap_count} sentences were missed out of {self.all_count} ({self.gap_count/self.all_count*100}% missed).")

