from csv import reader, writer, register_dialect
from pathlib import Path

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"
PREPROCESSED_DIR = HERE / "preprocessed"

register_dialect("")

if not PREPROCESSED_DIR.exists():
    PREPROCESSED_DIR.mkdir()

for x in DATA_DIR.iterdir():
    if x.suffix != ".csv":
        continue
    with x.open('r', encoding='UTF-8') as file:
        csv = reader(file, quotechar='"', delimiter=',')
        new_file = PREPROCESSED_DIR / x.name
        with new_file.open('w+', encoding='UTF-8', newline='') as processed_file:
            processed_csv = writer(processed_file, quotechar='"', delimiter=',')
            i = 0
            for line in csv:
                dialogue = line[3].lower().strip()
                if len(dialogue) == 0:
                    continue
                if i >= 1:
                    line[2] = str(i-1)
                i += 1
                processed_csv.writerow(line)



