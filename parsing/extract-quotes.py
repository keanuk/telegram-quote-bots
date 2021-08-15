#!/usr/bin/python

import sys
import json
import pickle
import re

quotes = {}

def extract_quotes(media_name):
	file = open("media-scripts/" + media_name + "/" + media_name + ".txt")
	lines  = file.readlines()
	i = 0
	while i < len(lines):
		# Skip lines which do not contain character names
		is_name = True
		for c in lines[i].strip():
			if c.isalpha() and not c.isupper():
				is_name = False
		if not is_name:
			i += 1
			continue

		if lines[i].startswith(" ") and lines[i + 1].startswith(" "):
			name = ''
			for word in lines[i].strip().split(" "):
				if word and word[0].isalpha():
					name += word + " "
				else:
					break
			quote = ''

			i += 1;

			while not lines[i].strip() or (lines[i].startswith(" ") and not lines[i].split()[0].isupper()):
				quote = quote + lines[i].strip() + " ";
				i += 1

			i -= 1

			# Removes text within parentheses, replaces multiple spaces with a single space, and removes trailing spaces
			name = re.sub(r'\([^)]*\)', '', ' '.join(name.strip().split()))
			quote = re.sub(r'\([^)]*\)', '', ' '.join(quote.strip().split()))
			if len(name) > 0 and len(quote) > 0:
				if name in quotes:
					quotes[name].append(quote)
				else:
					quotes[name] = [quote]
		i += 1
	file.close()

	with open('../models/' + media_name + '.json', 'w', encoding='utf8') as f:
		json.dump(quotes, f, ensure_ascii=False)

	with open('../models/' + media_name + '.pickle', 'wb') as f:
		pickle.dump(quotes, f)
	
	print("Success")

extract_quotes(sys.argv[1])