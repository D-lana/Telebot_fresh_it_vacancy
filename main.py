import telebot
from auth_data import token
from parser_data import *


def telegram_bot(token):
	bot = telebot.TeleBot(token)

	@bot.message_handler(commands=["start"])
	def start_message(message):
		answer = greeting + host_name + "!\n"
		answer += answer_list_cmd
		bot.send_message(message.chat.id, answer)
		

	@bot.message_handler(content_types=["text"])
	def send_text(message):
		skill, grade, *args = message.text.lower().split()
		try:
			s = get_answer(skill, grade)
			for item in s:
				bot.send_message(message.chat.id, item)
				print(item)
		except Exception as ex:
			bot.send_message(message.chat.id, fail_request)

	bot.polling()

def main():
	telegram_bot(token)

if __name__ == "__main__":
	main()
