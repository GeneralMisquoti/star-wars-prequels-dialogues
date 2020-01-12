import re

from quote import QuoteCleanPattern
from .globals import default_clean_patterns, default_ignored, default_blacklist, default_mappings, default_strict

quote_clean_patterns = default_clean_patterns + [QuoteCleanPattern(r'[\n\t]+', ' ')]
quote_pattern = re.compile(r'\t\t([A-ZÉ&0-9 \-\.]+)\n((?:\t+[\S ]+\n)+)')
character_pattern = re.compile(r'([A-ZÉ0-9][A-ZÉ&0-9 \-\.\']*[A-ZÉ0-9][A-ZÉ0-9])')
ignored = default_ignored + ["ZAM'S ARM"]
mappings = {
	'JANGO FETT': 'JANGO FETT',
	'JANGO': 'JANGO FETT',
	'SERVER': 'FOOD SERVER',
	'HERMIONE': 'HERMIONE BAGWA',
	**default_mappings
}
strict = default_strict
blacklist = default_blacklist
