from pathlib import Path

here_path = Path(__file__).parent
merged_dir_path = here_path / "merged"


top_dir = here_path.parent

parsed_scripts_dir_path = top_dir / "scripts" / "parsed_scripts"
fandom_links_file_path = parsed_scripts_dir_path / "characters_fandom" / "link_choices.json"
parsed_yarn_data_dir_path = top_dir / "yarn" / "parsing_source" / "parsed_sources" / "hand_fixed"
