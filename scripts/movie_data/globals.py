import re

from quote import QuoteCleanPattern

default_clean_patterns = [QuoteCleanPattern(re.compile(r'\(.*\)'), ''), QuoteCleanPattern(re.compile(r'  '), ' ')]
default_ignored = [
	'TITLE CARD', 'V.O', 'O.S', 'TOWARD CAMERA',
	'PAN DOWN', 'PAN', "EPISODE 1 THE PHANTOM MENACE", "PAST CAMERA"
]
default_strict = []
default_blacklist = ['INT.', 'EXT.', '- DAY', '- NIGHT', 'AFTERNOON', "DAWN"]
default_mappings = {
	'YODA': 'MASTER YODA',
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
	'MACE-WINDU': 'MACE WINDU',
	'THREEPIO': 'C-3PO',
	'ARTOO': 'R2-D2',
	'R2': 'R2-D2',
	'CLONE TROOPER': 'CLONE TROOPER',
	'REPRESENTATIVE JAR JAR BINKS': 'JAR JAR BINKS',
	'KI-ADI': 'KI-ADI-MUNDI',
	'PRINCE BAIL ORGANA': 'BAIL ORGANA',
	'SENATOR BAIL ORGANA': 'BAIL ORGANA',
	'VICE CHAIRMAN MAS AMEDDA': 'MAS AMEDDA',
	'A PILOT': 'PILOT'
}
