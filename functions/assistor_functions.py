import telebot
import json

database_file_path = "database/database.json"

def create_buttons(elements:list, width:int):
	'''
	creates buttons with the given elements in the list with the given width and returns a markup
	'''
	markup = telebot.types.ReplyKeyboardMarkup(row_width=width)

	if 1 < width <= 3 < len(elements):
		while len(elements) % 3 != 0:
			elements.append("")
		if width == 2:
			for i in range(0, len(elements), 2):
				btn1 = telebot.types.KeyboardButton(elements[i])
				btn2 = telebot.types.KeyboardButton(elements[i + 1])
				markup.add(btn1, btn2)

		if width == 3:
			for i in range(0, len(elements), 3):
				btn1 = telebot.types.KeyboardButton(elements[i])
				btn2 = telebot.types.KeyboardButton(elements[i + 1])
				btn3 = telebot.types.KeyboardButton(elements[i + 2])
				markup.add(btn1, btn2, btn3)

	else:
		for i in elements:
			btn = telebot.types.KeyboardButton(i)
			markup.add(btn)

	return markup

def refresh_database() -> dict:
	'''
	refreshes the database and returns the current data
	'''
	with open(database_file_path) as file:
		data = json.load(file)
	file.close()

	return data

def dump_database(data) -> None:
	'''
	dumps the current data in the bot temp collection into the database
	'''
	with open(database_file_path, mode='w') as file:
		json.dump(data, file)
	file.close()

def update_database(attribute:str, data) -> None:
	'''
	appends the database with the data into the given attribute
	'''
	old = refresh_database()
	old[attribute].append(data)
	dump_database(old)