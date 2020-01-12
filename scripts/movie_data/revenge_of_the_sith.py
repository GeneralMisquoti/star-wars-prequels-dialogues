import re

from quote import QuoteCleanPattern
from .globals import default_patterns, default_blacklist, default_ignored, default_mappings

quote_clean_patterns = default_patterns
quote_pattern = re.compile(r'^([A-Z\-\s0-9\.]+)\s*:\s*(.*$)')
character_pattern = re.compile(r'([A-Z0-9][A-Z0-9 \-\.\']*[A-Z0-9])')
ignored = default_ignored
mappings = default_mappings
blacklist = default_blacklist
