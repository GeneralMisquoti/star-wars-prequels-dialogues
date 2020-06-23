from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.analysis import StemmingAnalyzer
from whoosh import index, qparser
import json

from paths import here_path, merged_dir_path, top_dir
from movies import movies, WhichMovie, name_dict, movie_dict
from load_files import yarn_file_paths, parsed_scripts_file_paths, fandom_links_file_path

character_links = json.load(fandom_links_file_path.open('r', encoding='UTF-8'))
index_dir_path = here_path / "indexdir"

if not index_dir_path.exists():
	index_dir_path.mkdir()

schema = Schema(
	movie=NUMERIC(stored=True),
	character=NUMERIC(stored=True),
	quote=KEYWORD(stored=True),
)

ix = index.create_in(index_dir_path, schema)
writer = ix.writer()

print("Building index")

for script_file in parsed_scripts_file_paths:
	print(f'Building index for file "{script_file.relative_to(top_dir)}"')
	movie: WhichMovie = name_dict[script_file.stem]

	script_data = json.load(script_file.open('r', encoding="UTF-8"))
	print(f"Indexing ({movie}): ", end="")
	len_all_quotes = len(script_data['quotes'])
	for i, q in enumerate(script_data['quotes']):
		print(f"\r{(i+1)/len_all_quotes * 100:.2f}%", end='', flush=True)
		writer.add_document(movie=movie.value, character=q['character'], quote=q['quote'])
	print("")

print("Committing indexing...", end='')
writer.commit()
print("Done.")

with ix.searcher() as searcher:
	if not merged_dir_path.exists() or not merged_dir_path.is_dir():
		merged_dir_path.mkdir()

	qp = qparser.QueryParser("quote", schema=ix.schema, group=qparser.OrGroup)

	for yarn_file in yarn_file_paths:
		print(f'Opening yarn data file "{yarn_file.relative_to(top_dir)}"')

		movie: WhichMovie = name_dict[yarn_file.stem]

		yarn_data = json.load(yarn_file.open('r', encoding="UTF-8"))
		print(f'Loading quotes: ', end='')
		len_all_quotes = len(yarn_data)
		for i, q in enumerate(yarn_data):
			quote_text = q['transcript']
			print(f'\r{(i+1)/len_all_quotes*100:.2f}%', end='', flush=True)
			"""
			Split '- This time we will do it together. - I was about to say that.'
			into -> ['This time we will do it together.', 'I was about to say that.']
			"""
			for x in quote_text.split('-'):
				single_quote = x.strip()
				if single_quote != "":
					q = qp.parse(single_quote, normalize=False)
					results = searcher.search(q)
					pass
		print("")






