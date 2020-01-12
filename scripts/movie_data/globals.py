import re

from quote import QuoteCleanPattern

default_patterns = [QuoteCleanPattern(re.compile(r'\(.*\)'), ''), QuoteCleanPattern(re.compile(r'  '), ' ')]
default_ignored = [
	'TITLE CARD', 'V.O', 'O.S', 'TOWARD CAMERA',
	'PAN DOWN', 'PAN', "EPISODE 1 THE PHANTOM MENACE", "PAST CAMERA"
]
default_blacklist = ['INT. ', 'EXT. ', '- DAY', '- NIGHT']
default_mappings = {
	'DOFINE': 'CAPTAIN DAULTRAY DOFINE',
	'PALPATINE': 'SUPREME CHANCELLOR PALPATINE',
	'QUI-GON': 'QUI-GON JINN',
	'QUI GON': 'QUI-GON JINN',
	'OBI-WAN': 'OBI-WAN KENOBI',
	'OBI WAN': 'OBI-WAN KENOBI',
	'AMIDALA': 'PADMÉ NABERRIE AMIDALA',
	'PADMÉ': 'PADMÉ NABERRIE AMIDALA',
	'PADME': 'PADMÉ NABERRIE AMIDALA',
	'ANAKIN': 'ANAKIN SKYWALKER',
	'PANAKA': 'CAPTAIN PANAKA',
	'TARPALS': 'CAPTAIN TARPALS',
	'MACE-WINDU': 'MACE WINDU'
}
