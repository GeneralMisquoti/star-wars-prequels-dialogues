# Create pairings of files
from scripts.movies import movies
from paths import fandom_links_file_path, parsed_scripts_dir_path, parsed_yarn_data_dir_path

assert len(movies) == 3

assert parsed_yarn_data_dir_path.exists()
yarn_file_paths = list(parsed_yarn_data_dir_path.glob('*.json'))
assert len(yarn_file_paths) == len(movies)

assert parsed_scripts_dir_path.exists()
parsed_scripts_file_paths = list(parsed_scripts_dir_path.glob('*.json'))
assert len(parsed_scripts_file_paths) == len(movies)

assert fandom_links_file_path.exists()
