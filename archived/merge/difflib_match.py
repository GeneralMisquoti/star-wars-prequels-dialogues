# https://stackoverflow.com/a/17741165/10854888

import difflib


def difflib_match(shorter: str, longer: str):
	s = difflib.SequenceMatcher(None, longer, shorter)
	match = ''.join(longer[i:i+n] for i, j, n in s.get_matching_blocks())
	return len(match) / len(shorter), match
