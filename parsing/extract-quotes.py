#!/usr/bin/python

import sys

quotes = {}

def extract_quotes(media_name):
	file = open("media-scripts/" + media_name + "/" + media_name + ".txt")
	lines  = file.readlines();
	i = 0;
	while i < len(lines):
		if lines[i].startswith(" ") and lines[i + 1].startswith(" "):
			title = lines[i].strip().split(" ");
			name = "";
			for word in title:
				if word and word[0].isalpha():
					name += word + " ";
				else:
					break;
			quote = '';
			i += 1;
			while lines[i].startswith(" "):
				quote = quote + lines[i].strip() + " ";
				i += 1;
			name = name.strip();
			quote = quote.strip();
			if len(name) > 0 and len(quote) > 0:
				if name in quotes:
					quotes[name].append(quote);
				else:
					# print("New character " + name + " with quote " + quote);
					quotes[name] = [quote];
		i += 1;
	file.close();

	for key, value in quotes.items():
		print(key + ": " + str(value));





extract_quotes(sys.argv[1])