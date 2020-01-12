import re

from quote import QuoteCleanPattern
from .globals import default_patterns, default_ignored, default_blacklist, default_mappings

quote_clean_patterns = default_patterns + [QuoteCleanPattern(r'[\n\t]+', ' ')]
quote_pattern = re.compile(r'\t\t([A-ZÉ0-9 \-\.]+)\n((?:\t+[\S ]+\n)+)')
character_pattern = re.compile(r'([A-ZÉ0-9][A-ZÉ0-9 \-\.\']*[A-ZÉ0-9][A-ZÉ0-9])')
ignored = default_ignored
mappings = default_mappings
blacklist = default_blacklist
