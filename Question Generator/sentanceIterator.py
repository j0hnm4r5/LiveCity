import requests
from thesaurusCredentials import *
import re

from time import sleep


# SIX WORDS IS ABOUT THE MAXIMUM (TAKES ABOUT 1 MIN).
sentence = "How does a modern city appear?"
# sentence = "One, two, three, four, five, six, seven"

punctuation = ' !.,?'
sentence_list = re.split('([' + punctuation +'])', sentence)
for x in range(sentence_list.count(' ')):
	sentence_list.remove(' ')

print sentence_list

word_list = []
for x in range(len(sentence_list)):
	word_list.append([sentence_list[x]])

for q, word in enumerate(sentence_list):
	arguments = {'version':'2', 'api_key':THESAURUS_KEY, 'word':word, 'format':'json'}
	r = requests.get('http://words.bighugelabs.com/api/{version}/{api_key}/{word}/{format}'.format(**arguments))

	if r.status_code == (200 or 303):
		formatted = r.json()
		parts = formatted.keys()

		for i, part_of_speech in enumerate(parts):
			for category in formatted[part_of_speech]:
				for term in formatted[part_of_speech][category]:
					word_list[q].append(term)
					# print term

	elif r.status_code == 404:
		# print "Word not found"
		pass
	elif r.status_code == 500:
		# print "API usage exceeded. Wait until tomorrow."
		pass

print "ALL WORDS GATHERED"

import itertools
new_sentences = list(itertools.product(*word_list))
for item in new_sentences:
	print " ".join(item)
	sleep(.1)
