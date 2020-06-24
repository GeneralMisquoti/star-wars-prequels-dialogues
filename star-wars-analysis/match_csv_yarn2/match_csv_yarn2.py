import logging
from time import strftime

from pathlib import Path
from .utils.file_json import JsonFile
from .utils.file_csv import CsvFile
from .utils.overrides import Overrides, GlobalOverride
from .utils.gaps import DetectGaps


HERE = Path(__file__).parent

# Logging
LOGGING_DIR = HERE / "logs"
if not LOGGING_DIR.exists():
    LOGGING_DIR.mkdir()
log_file = LOGGING_DIR / (strftime("%y_%m_%d_%H_%M_%S") + ".log")
file_handler = logging.FileHandler(
    filename=log_file,
)
file_handler.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(
)
stream_handler.setLevel(logging.ERROR)
logging.basicConfig(
    handlers=[file_handler, stream_handler],
    format='[%(asctime)s,%(msecs)d] %(levelname)s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
module_logger = logging.getLogger(__name__)
module_logger.info('Starting this bitch.')

CSV_DATA_DIR = HERE.parent / "preprocessed"
YARN_DATA_DIR = HERE.parent.parent / "yarn" / "parsing_source" / "parsed_sources" / "hand_fixed"
OVERRIDES_DIR = HERE / "manual_overrides"
GLOBAL_OVERRIDE = GlobalOverride(OVERRIDES_DIR / "global.toml")

MOVIE_NAMES = ["phantom_menace", "attack_of_the_clones", "revenge_of_the_sith"]
CSV_FILES = [
    CsvFile(
        CSV_DATA_DIR / (f"{i+1:02}_" + movie_name + ".csv"),
        Overrides(
            dir=OVERRIDES_DIR / movie_name,
            global_override=GLOBAL_OVERRIDE),
        movie_index=i
    ) for i, movie_name in enumerate(MOVIE_NAMES)
]
JSON_FILES = [
    JsonFile(
        YARN_DATA_DIR / (movie_name + ".json"),
        movie_index=i
    ) for i, movie_name in enumerate(MOVIE_NAMES)
]
ZIPPED_FILES = list(zip(CSV_FILES, JSON_FILES))

assert len(ZIPPED_FILES) != 0

for i, (csv, yarn) in enumerate(ZIPPED_FILES):
    csv.find_matches(
        yarn,
        show_progress=True,
        detect_gaps=DetectGaps(log_file.with_name(log_file.stem + f"_gaps_{i}.txt"), movie=yarn.movie)
    )


OUTPUT_DIR = HERE / "output"
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

OUTPUT_FILES_PROD = [OUTPUT_DIR / (movie_name + ".csv") for movie_name in MOVIE_NAMES]
for out_file, (csv_file, yarn_file) in zip(OUTPUT_FILES_PROD, ZIPPED_FILES):
    with out_file.open('w+', encoding='UTF-8', newline='') as file:
        csv_file.write(file, test=False)

OUTPUT_FILES_TEST = [OUTPUT_DIR / (movie_name + ".test.csv") for movie_name in MOVIE_NAMES]
for out_file, (csv_file, yarn_file) in zip(OUTPUT_FILES_TEST, ZIPPED_FILES):
    with out_file.open('w+', encoding='UTF-8', newline='') as file:
        csv_file.write(file, test=True)
