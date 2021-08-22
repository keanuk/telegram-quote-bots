import sys
import logging
import random
import re
import json
import csv
import string
from collections import Counter
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

screenplay_path = "../media-scripts/"
character_path = "../models/characters/"
all_characters_path = "../models/all-characters/"
triggers_path = "../models/triggers/"
context_mappings_path = "../models/context-mappings/"
common_path = "../supplimentary/common.csv"

quotes = []
triggers = []
context_mapping = {}

def start(update, context):
	global quotes
	context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(quotes))

def reply(update, context):
	global quotes
	global triggers
	if (any(word in (update.message.text).lower() for word in triggers)):
		reply = random.choice(quotes)
		words = (update.message.text).lower().split()
		random.shuffle(words)
		for word in words:
			filtered = re.sub(r'/[^0-9A-Za-z\'-]/', '', re.sub('[`‘’’]', '\'', word.lower()).strip(string.punctuation).strip('\'\"“”'))
			if filtered in context_mapping.keys():
				reply = random.choice(context_mapping[filtered])				
		context.bot.send_message(chat_id = update.effective_chat.id, text = reply)

def load_quotes(character):
	global character_path
	with open(character_path + character.lower() + ".csv", 'r') as f:
		reader = csv.reader(f)
		return list(reader)[0]

def load_triggers(character):
	global triggers_path
	with open(triggers_path + character.lower() + ".csv", 'r') as f:
		reader = csv.reader(f)
		return list(reader)[0]

def load_context_mapping(character):
	global context_mappings_path
	return json.load(open(context_mappings_path + character.lower() + ".json", "r"))

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

def main(media, character, bot):
	global quotes
	global triggers
	global context_mapping

	f = open("../tokens/" + bot + ".txt", "r")
	apiToken = f.read().replace('\n', '')

	updater = Updater(token = apiToken, use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

	quotes = load_quotes(character)
	triggers = load_triggers(character)
	context_mapping = load_context_mapping(character)

	print("Starting bot\nCharacter name: " + character + "\n" + "Quotes:")
	print(random.choice(quotes))

	start_handler = CommandHandler('start', start)
	reply_handler = MessageHandler(Filters.text, reply)

	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(reply_handler)

	updater.start_polling()

main(sys.argv[1], sys.argv[2], sys.argv[3])