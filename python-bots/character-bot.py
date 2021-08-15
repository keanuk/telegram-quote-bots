import sys
import logging
import random
import json

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

quotes = {}
triggers = {}
character = ""

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="What?")

def reply(update, context):
	if (any(word in (update.message.text).lower() for word in {"thomas", "tom", "tommy", "lobster", "winslow",
	 "secret", "wake", "what", "wot", "wat", "steak", "aye", "lad", "drink", "drunk", "ye", "hark", "triton",
	 "neptune", "gull", "toast", "steady", "luck", "damn", "cook"})):
		reply = random.choice(quotes[character])
		context.bot.send_message(chat_id = update.effective_chat.id, text = reply)

def main(media, name, bot):
	global quotes
	global triggers
	global character

	f = open("../tokens/" + bot + ".txt", "r")
	apiToken = f.read().replace('\n', '')

	updater = Updater(token = apiToken, use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

	quotes = json.load(open("../models/" + media + ".json", "r"))
	character = name.upper();

	print("Starting bot\nCharacter name: " + character + "\n" + "Quotes:")
	print(random.choice(quotes[character]))

	start_handler = CommandHandler('start', start)
	reply_handler = MessageHandler(Filters.text, reply)

	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(reply_handler)

	updater.start_polling()

main(sys.argv[1], sys.argv[2], sys.argv[3])