from pathlib import Path
from typing import List
import json

here = Path(__file__).parent
parsed_sources = here / "parsed_sources"
if not parsed_sources.is_dir() or not parsed_sources.exists():
	parsed_sources.mkdir()
source_dir: Path = here.parent

videos_ids = set()
videos = {}


def parse_json(file_path: Path):
	global videos_ids
	global videos
	
	assert file_path.parent == source_dir
	json_data = json.load(file_path.open('r', encoding="UTF-8"))
	json_data: List[dict]
	json_data = list(filter(lambda x: x["interaction_type"] == "transcript", json_data))
	for quote in json_data:
		video = quote['Video']
		if isinstance(video, dict):
			id = video['id']
			if id not in videos_ids:
				del video['num_people']
				del video['num_slides']
				del video['top_concepts']
				del video['human_time']
				del video['group_id']
				del video['segment_600']
				del video['team_id']
				del video['user_id']
				del video['num_words']
				del video['num_unique_words']
				del video['transcript']
				videos_ids.add(id)
				videos[id] = video
			quote['Video'] = id
			del quote['slide_url']
			del quote['slide']
			del quote['sentiment_score']
			del quote['sentiment_type']
			del quote['user_id']
			del quote['team_id']
			del quote['cld']
	return json_data


for file in source_dir.glob('*.json'):
	file: str
	file_path = source_dir / file
	movie_data = parse_json(file_path)
	movie_data.sort(key=lambda x: x['start_time'])
	json.dump(movie_data, open(parsed_sources / file, 'w+', encoding="UTF-8"), ensure_ascii=False)

json.dump(videos, open(parsed_sources / "videos.json", 'w+', encoding="UTF-8"), ensure_ascii=False)

