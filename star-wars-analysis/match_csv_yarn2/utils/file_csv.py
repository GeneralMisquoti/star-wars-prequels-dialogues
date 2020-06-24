from .utils.file_abstract import File
from .row_csv import CsvRow
from .file_json import JsonFile
from .overrides import Overrides
from .gaps import DetectGaps

from pathlib import Path
from csv import reader, writer
import logging

module_logger = logging.getLogger(__name__)


class CsvFile(File):
    def __init__(self, path: Path, overrides: Overrides, movie_index: int):
        self.overrides = overrides
        super().__init__(path, movie_index, overrides=overrides)
        csv_parsed = reader(path.open('r', encoding='UTF-8'), quotechar='"', delimiter=',')

        # Skip header
        csv_parsed.__next__()

        super().parse(csv_parsed, CsvRow)

    def __iter__(self):
        return self._iter.__iter__()

    def find_matches(self, json_file: JsonFile, show_progress=False, detect_gaps: DetectGaps = None):
        this_movie = self.movie
        other_movie = json_file.movie
        last_match_id = 0

        # For sentence in this movie
        for i, sentence in enumerate(this_movie.sentences):
            permission = self.overrides.give_permission(sentence)
            if not permission.allow:
                continue
            if not permission.force_id:
                try_replace = self.overrides.should_try_replace(sentence)
                for other_sentence in other_movie.sentences[last_match_id:]:
                    sentence.match(other_sentence, alternative_text=try_replace)
                    match = sentence.best_match
                    if (match.ideal_match and len(sentence.matches) >= sentence.THRESHOLD_CHECK_MORE_FOR_FUN) \
                       or match.wont_be_better:
                        break
            else:
                # Force match rows
                rows = []
                for forced_id in permission.force_id:
                    try:
                        forced_rows = []
                        range_sentences = other_movie.sentences[last_match_id:]
                        if range_sentences[0].parent_row.yarn_id > forced_id:
                            raise Exception('wtf')
                        for x in range_sentences:
                            if x.parent_row.yarn_id == forced_id:
                                forced_rows.append(x.parent_row)
                                break
                        if len(forced_rows) > 0:
                            rows.extend(forced_rows)
                            last_match_id = forced_rows[-1].id
                    except StopIteration:
                        print()
                        module_logger.fatal(
                            f"STOPITERATION: {self.movie.name} Not found"
                            f"id {forced_id} in range [{last_match_id}:] "
                        )
                        exit()
                sentence.force_matches(rows)
                detect_gaps.take_note_of_forced_rows(sentence)
            last_match = sentence.decide_on_match()
            if detect_gaps and last_match:
                # TODO: detect gap and try to mitigate somehow, break on commas etc.
                gap = detect_gaps.detect(last_match, sentence, movie_index=self.movie.index)
            if last_match:
                last_match_id = last_match.other.id

            # For debugger introspection
            prev_sentence = sentence
            if show_progress:
                print(f'\r{i+1:04}/{len(this_movie.sentences):04}', end="")
        if show_progress:
            print()

        if detect_gaps:
            detect_gaps.log_count()

    def write(self, file, test=False):
        to_be_dumped = []
        if test:
            for row in self.movie.rows:
                headers, new_dump = row.to_map_test()
                to_be_dumped.extend(new_dump)
        else:
            for row in self.movie.rows:
                headers, new_dump = row.to_map_prod()
                to_be_dumped.extend(new_dump)

        csv_writer = writer(file)
        csv_writer.writerow(headers)
        csv_writer.writerows(to_be_dumped)
