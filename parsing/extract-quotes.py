#!/usr/bin/python

import sys
import os
import json
import csv
import re
import string
from collections import Counter

screenplay_path = "../media-scripts/"
character_path = "../models/characters/"
all_characters_path = "../models/all-characters/"
triggers_path = "../models/triggers/"
context_mappings_path = "../models/context-mappings/"
common_path = "../supplimentary/common.csv"

def load_common():
	global common_path
	common = []
	with open(common_path, 'r') as f:
		reader = csv.reader(f)
		common = list(reader)[0]
	common_filtered = []
	for word in common:
		common_filtered.append(re.sub(r'/[^0-9A-Za-z\'-]/', '', word.lower()))
	return common_filtered

def get_commonly_used_words(quotes):
	common = load_common()
	words = []
	for quote in quotes:
		for word in quote.split():
			filtered = re.sub(r'/[^0-9A-Za-z\'-]/', '', re.sub('[`‘’’]', '\'', word.lower()).strip(string.punctuation).strip('\'\"“”'))
			if filtered not in common and len(filtered) > 0:
				words.append(filtered)
	return [word for word, word_count in Counter(words).most_common(20)]

def create_context_mappings(quotes, triggers):
	common = load_common()
	context_mappings = {}
	for quote in quotes:
		for word in quote.split():
			filtered = re.sub(r'/[^0-9A-Za-z\'-]/', '', re.sub('[`‘’’]', '\'', word.lower()).strip(string.punctuation).strip('\'\"“”'))
			if (filtered not in common) and (filtered not in triggers):
				if filtered in context_mappings:
					context_mappings[filtered].append(quote)
				else:
					context_mappings[filtered] = [quote]
	return context_mappings

def write_context_mappings(character_name, quotes, triggers):
	global context_mappings_path
	context_mappings = create_context_mappings(quotes[character_name.upper()], triggers)
	with open(context_mappings_path + character_name.lower() + '.json', 'w', encoding='utf8') as f:
		json.dump(context_mappings, f, ensure_ascii=False)

def write_triggers(character_name, quotes):
	global triggers_path
	triggers = get_commonly_used_words(quotes[character_name.upper()])
	triggers.append(character_name.lower())
	with open(triggers_path + character_name.lower() + '.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(triggers);
	return triggers

def write_all_to_file(media_name, quotes):
	global all_characters_path
	with open(all_characters_path + media_name.lower() + '.json', 'w', encoding = 'utf8') as f:
		json.dump(quotes, f, ensure_ascii = False)

def write_to_file(character_name, quotes):
	global character_path
	with open(character_path + character_name.lower() + '.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(quotes[character_name.upper()]);

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
	write_to_file(character_name, quotes)
	triggers = write_triggers(character_name, quotes)
	write_context_mappings(character_name, quotes, triggers)

	print("Success")

extract_quotes(sys.argv[1], sys.argv[2])