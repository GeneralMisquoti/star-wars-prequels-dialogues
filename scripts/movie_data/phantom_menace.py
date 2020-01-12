import re

from .globals import default_clean_patterns, default_blacklist, default_ignored, default_mappings, default_strict

quote_clean_patterns = default_clean_patterns
quote_pattern = re.compile(r'^([A-ZÉ0-9][A-ZÉ\-\.& ]+)\s*:\s*(.*$)', flags=re.MULTILINE)
character_pattern = re.compile(r'([A-ZÉ0-9][A-Z&É0-9 \-\.\']*[A-ZÉ0-9][A-ZÉ0-9])', flags=re.MULTILINE)
ignored = default_ignored + ['DROID SARGEANT', 'EXPLOSION', 'EIRTAE', 'PROTOCOL DROID',
	 'SANDO AQUA MONSTER', 'JAR', 'WHEN YOUSA TINK WESA IN TROUBLE', '327 N', '523 A', '000 R',
	 'BATTLE DROIDS', 'WHEEL DROIDS', 'SECOND QUEEN']
mappings = default_mappings
blacklist = default_blacklist
strict = default_strict
# short_characters = {"A", "B"}
