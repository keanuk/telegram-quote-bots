#!/usr/bin/python

import sys
import os
import json
import csv
import re

screenplay_path = "../media-scripts/"
character_path = "../models/characters"
all_characters_path = "../models/all-characters"
triggers_path = "../models/triggers"

def write_all_to_file(media_name, quotes):
	global all_characters_path
	with open(all_characters_path + media_name + '.json', 'w', encoding = 'utf8') as f:
		json.dump(quotes, f, ensure_ascii = False)

def write_to_file(character_name, quotes):
	global character_path
	with open(character_path + character_name + '.csv', 'w', encoding = 'utf8') as f:
		csv.writer.writerow(quotes[character_name]);

def extract_quotes(media_name, character_name):
	global screenplay_path
	quotes = {}
	with os.scandir(screenplay_path + media_name) as target:
		for entry in target:
			if entry.name.endswith(".txt") and entry.is_file():	
				file = open(screenplay_path + media_name + "/" + entry.name, "r")
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

	write_all_to_file(media_name, quotes)
	write_to_file(media_name, quotes)

	print("Success")

extract_quotes(sys.argv[1])