import re

from .globals import default_clean_patterns, default_blacklist, default_ignored, default_mappings, default_strict

quote_clean_patterns = default_clean_patterns
quote_pattern = re.compile(r'^([A-ZÉ0-9][A-ZÉ&\-\. ]+)\s*:\s*(.*$)', re.MULTILINE)
character_pattern = re.compile(r'([A-ZÉ0-9][A-Z&É0-9 \-\.\']*[A-ZÉ0-9][A-ZÉ0-9])')
ignored = default_ignored + ["HOLOGRAM OF DARTH SIDIOUS", "HUNDREDS OF CLONE TROOPERS"]
mappings = {
	'CLONE SERGEANT': 'CLONE SERGEANT',
	'BATTLE DROID': 'BATTLE DROID',
	**default_mappings
}
strict = default_strict + ["CLONE SERGEANT", "BATTLE DROID"]
blacklist = default_blacklist
