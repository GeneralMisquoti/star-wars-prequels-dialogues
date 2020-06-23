from pathlib import Path
import json
import csv
from pprint import pprint

here = Path(__file__).parent
sources_dir = here.parent
output_path = here / "to_whom_output"

if not output_path.exists():
    output_path.mkdir()


def main():
    for file in sources_dir.glob('*.json'):
        speech_file = json.load(file.open('r', encoding='UTF-8'), encoding='UTF-8')
        characters = speech_file['characters']
        with open(here / (str(file.stem) + ".csv"), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                print(f"row: {row}")
                for s_row in speech_file['quotes']:
                    if row[3].strip() == "":
                        continue
                    if row[3] in s_row['quote']:
                        s_row: dict
                        character_json = characters[s_row['character']]
                        if row[0].lower() not in character_json.lower():
                            pass
                        #print(f"Csv \"{row[0]}\" character doesn't match with json \"{character_json}\". File: {file}; line: {row[3]}, {s_row['quote']}")
                        s_row.setdefault('to', set())
                        s_row['to'].add(row[1])
            for quote in speech_file['quotes']:
                quote: dict
                if quote.get('to') is not None:
                    quote['to'] = list(quote['to'])
        json.dump(speech_file, (output_path / (file.stem + ".json")).open('w+', encoding="UTF-8"), ensure_ascii=False)


if __name__ == "__main__":
    main()

