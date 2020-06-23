from csv import reader, writer
from .utils.file_abstract import File
from .row_csv import CsvRow
from pathlib import Path
from .file_json import JsonFile
from .overrides import Overrides
import logging

module_logger = logging.getLogger(__name__)


class CsvFile(File):
    def __init__(self, path: Path, overrides: Overrides):
        super().__init__(path)
        csv_parsed = reader(path.open('r', encoding='UTF-8'), quotechar='"', delimiter=',')
        self.overrides = overrides

        # Skip header
        csv_parsed.__next__()

        super().parse(csv_parsed, CsvRow)

    def __iter__(self):
        return self._iter.__iter__()

    def find_matches(self, json_file: JsonFile, show_progress=False):
        this_movie = self.movie
        other_movie = json_file.movie
        last_match_id = 0

        # For sentence in this movie
        for i, sentence in enumerate(this_movie.sentences):
            permission = self.overrides.give_permission(sentence)
            if not permission.allow:
                continue
            if not permission.force_id:
                for other_sentence in other_movie.sentences[last_match_id:]:
                    sentence.match(other_sentence)
                    match = sentence.best_match
                    if (match.ideal_match and len(sentence.matches) >= sentence.THRESHOLD_CHECK_MORE_FOR_FUN) \
                       or match.wont_be_better:
                        break
            else:
                # FIXME: Id is of row, but we choose sentence
                sentences = []
                for forced_id in permission.force_id:
                    try:
                        forced_sentence = next(
                            x for x in other_movie.sentences[last_match_id:] if x.parent_row.yarn_id == forced_id
                        )
                        sentences.append(forced_sentence)
                        last_match_id = forced_sentence.id
                    except StopIteration:
                        print()
                        module_logger.fatal(f"STOPITERATION: {self.movie.name} Not found id {forced_id} in range [{last_match_id}:] ")
                        exit()
                sentence.force_matches(sentences)
            last_match = sentence.decide_on_match()
            if last_match:
                last_match_id = last_match.other.id

            # For debugger introspection
            prev_sentence = sentence
            if show_progress:
                print(f'\r{i+1:04}/{len(this_movie.sentences):04}', end="")
        if show_progress:
            print()

    def write(self, file):
        to_be_dumped = []
        for row in self.movie.rows:
            headers, new_dump = row.to_map_prod()
            to_be_dumped.extend(new_dump)

        csv_writer = writer(file)
        csv_writer.writerow(headers)
        csv_writer.writerows(to_be_dumped)
