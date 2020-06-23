from pathlib import Path
import csv
import argparse

here = Path(__file__).parent




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fix some ids')
    parser.add_argument('file',
                        help='the file to fix')
    args = parser.parse_args()
    in_file = here / args.file
    out_file = in_file
    bkup_file = in_file
    bkup_file = bkup_file.with_suffix(f'{bkup_file.suffix}.bkup')

    if not in_file.exists():
        in_file = bkup_file

    i = 0
    if not bkup_file.exists():
        bkup_file = bkup_file.with_suffix(f'{bkup_file.suffix}{i}')
    original = in_file.read_bytes()
    bkup_file.write_bytes(original)

    i = 1
    reader = csv.reader(in_file.open('r', encoding="UTF-8"))
    rows = [reader.__next__()]
    for row in reader:
        row[2] = i
        rows.append(row)
        i += 1
    writer = csv.writer(out_file.open('w', encoding="UTF-8", newline=''))
    writer.writerows(rows)

    print(f'File: "{in_file}"')
