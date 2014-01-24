import requests
from thesaurusCredentials import *

""" Available parts of speech include: Noun, Verb, Adjective, Adverb """
""" syn:synonyms, ant:antonyms, rel:related, sim:similar, usr:user-suggestions """


word = "quick"

arguments = {'version':'2', 'api_key':THESAURUS_KEY, 'word':word, 'format':'json'}

r = requests.get('http://words.bighugelabs.com/api/{version}/{api_key}/{word}/{format}'.format(**arguments))

if r.status_code == (200 or 303):
	formatted = r.json()
	parts = formatted.keys()

	print word
	for i, part_of_speech in enumerate(parts):
		print part_of_speech.upper()
		for category in formatted[part_of_speech]:
			print category, "***"
			for term in formatted[part_of_speech][category]:
				print term
		print "***********"
elif r.status_code == 404:
	print "Word not found"
elif r.status_code == 500:
	print "API usage exceeded. Wait until tomorrow."