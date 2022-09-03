import telebot
from common_files.commons import *
from functions.assistor_functions import *

API = "secret_bot_api"
ADMINS_ID = []

bot = telebot.TeleBot(API)

mode = 0
data = {}

@bot.message_handler(commands=['start'])
def start(message):
	global ADMINS_ID
	data = refresh_database()
	ADMINS_ID = data["admins"] # in order to be an admin, add your telegram id to the "admins" into database.json
	if message.chat.id in ADMINS_ID:
		bot.send_message(message.chat.id, "Welcome admin.", reply_markup=admin_home_markup)
	else:
		bot.send_message(message.chat.id, "Welcome to the association, dear member.", reply_markup=user_home_markup)

@bot.message_handler(content_types=['text'])
def serve(message):
	global mode, data
	if back_button_emoji in message.text:
		'''
		if there is a back_button_emoji in the text sent by the user, it means the user wants to go back to the start page as there is only 2 layers of pages in the bot interface
		''' 
		start(message)

	elif message.chat.id in ADMINS_ID:
		'''
		message.chat.id is the telegram user account id of the user, if that exists in the database as an admin id, treat them differently 
		'''
		if admin_question_emoji in message.text or info_emoji in message.text:
			'''
			so there is two things an admin could do, one is retrieve different information from the database, the other is to add new information to the database. The admin can add either a new question (to be shown to members) or can add new information to be displayed to users. If either has been selected, redirect them here.
			'''
			mode = 1 if admin_question_emoji in message.text else 5 # there are five modes for the admin, set respectively
			bot.reply_to(message, "Send here.", reply_markup=back_markup)

		elif answer_emoji in  message.text or comment_emoji in message.text or question_emoji in message.text:
			'''
			handles the other modes for the admin
			'''
			data = refresh_database()
			if answer_emoji in message.text:
				mode = 2
				for i in data["answers"]:
					bot.forward_message(message.chat.id, i[0], i[1])
				bot.reply_to(message, "These were the answers by the members to the current question.")
			elif comment_emoji in message.text:
				mode = 3
				for i in data["comments"]:
					bot.forward_message(message.chat.id, i[0], i[1])
				bot.reply_to(message, "These were the comments given up untill now.")
			elif question_emoji in message.text:
				mode = 4
				for i in data["user_questions"]:
					bot.forward_message(message.chat.id, i[0], i[1])
				bot.reply_to(message, "These were the questions forwarded from users.")
		else:
			'''
			if any other text is sent by the admin, it is probably to add questions or information, handle that accordingly
			'''
			if mode == 1:
				update_database("questions", message.text)
				bot.reply_to(message, "The new question has been saved.")
			elif mode == 5:
				update_database("common_information", message.text)
				bot.reply_to(message, "The new information has been saved.")
				
	else:
		'''
		if there is no back button in the user sent text (regardless of being an admin) and if their admin is not is the admins id list, then they are members, this else statement handles them
		'''
		if answer_emoji in message.text:
			mode = 1
			if not data: data = refresh_database() # so when retrieving data, if the data is already loaded, there is no need to load the whole database.json, it is time-consuming and also space consuming as jsons tend to be big in size
			bot.reply_to(message, "The current question is፡ {}".format(data["questions"][-1]))
			bot.send_message(message.chat.id, "Send your answer here.", reply_markup=back_markup)
		elif comment_emoji in message.text:
			mode = 2
			bot.reply_to(message, "Send your comment here.", reply_markup=back_markup)
		elif question_emoji in message.text:
			mode = 3
			bot.reply_to(message, "Send your question here.", reply_markup=back_markup)
		elif info_emoji in message.text:
			mode = 4
			if not data: data = refresh_database()
			for information in data["common_information"]:
				bot.send_message(message.chat.id, information)
			bot.reply_to(message, "These are the current information forwarded from administrators.", reply_markup=back_markup)

		else:
			# the variable attribute here is for code reusability since only the attribute changes in the message to be sent back to the user.
			attribute = None
			if mode == 0: start(message) # if the mode is still zero for some reason, return them back to the front page
			elif mode == 1: attribute = "answers"
			elif mode == 2: attribute = "comments"
			elif mode == 3: attribute = "user_questions"
			update_database(attribute, [message.chat.id, message.id])
			mode_names = ["answer", "comment", "question"]
			bot.reply_to(message, "Your {} has been saved. Thank you.".format(mode_names[mode-1]), reply_markup=user_home_markup)

bot.infinity_polling()