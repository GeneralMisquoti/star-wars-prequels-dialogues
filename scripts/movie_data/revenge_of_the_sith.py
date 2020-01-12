import re

from quote import QuoteCleanPattern
from .globals import default_patterns, default_blacklist, default_ignored, default_mappings

quote_clean_patterns = default_patterns
quote_pattern = re.compile(r'^([A-ZÉ0-9][A-ZÉ\-\. ]+)\s*:\s*(.*$)', re.MULTILINE)
character_pattern = re.compile(r'([A-ZÉ0-9][A-ZÉ0-9 \-\.\']*[A-ZÉ0-9][A-ZÉ0-9])')
ignored = default_ignored
mappings = {
	**default_mappings
}
blacklist = default_blacklist
