import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from info import *
from request_formation import request_formation, check_correct_data
import os

# библиотека BeautifulSoup предназначена для парсинга
# объектов html в удобные python объекты


def get_id_vacancy(link) ->str:
	id_vacancy = link.split("/")[-1]
	return id_vacancy


def get_data_from_habr(user_agent, lang, grade) ->BeautifulSoup:
	headers = {"user-agent": user_agent}
	url = request_formation(lang, grade)
	r = requests.get(url=url, headers=headers)
	soup = BeautifulSoup(r.text, "lxml")
	return soup


def parser_data_of_habr_career(soup, dict_vacancy) ->None:
	# получение данных из вакансии Хабр
	current_time = datetime.now()
	articles_cards = soup.find_all("div", class_="vacancy-card__inner")

	for article in articles_cards: #bs4.element.Tag - type
		title = article.find("a", class_="vacancy-card__title-link").text
		keys = article.find_all("a", class_="link-comp link-comp--appearance-dark")
		link = article.find("a", class_="vacancy-card__icon-link").get("href")
		time_pub = datetime.strptime(article.find("time").get("datetime"), '%Y-%m-%dT%H:%M:%S%z')
		dict_vacancy[get_id_vacancy(link)] = {
			"title": title,
			"link": url_habr + link,
			"keys": [k.text for k in keys],
			"time_pub": f"{time_pub.hour}:00 {time_pub.date()} "
		}


def get_data_of_vacancy(lang, grade):
	# Создаем словарь вакансий
	dict_vacancy = {}
	dict_old = {}
	# получение странички Хабр и сохранение в словарь
	soup = get_data_from_habr(user_agent, lang, grade)
	parser_data_of_habr_career(soup, dict_vacancy)

	# Загружаем старые данные и удаляем уже существующие вакансии
	name_file = dir_for_dicts_vacancy + "_".join([lang, grade, "dict.json"])
	if os.path.exists(dir_for_dicts_vacancy) == 0:
		os.mkdir(dir_for_dicts_vacancy)
	if os.path.exists(name_file) and os.stat(name_file).st_size != 0:
		with open(name_file, "r", encoding='utf-8') as file:
			dict_old = json.load(file)
			for key in dict_old:
				if key in dict_vacancy:
					del dict_vacancy[key]
			
	# Записываем в JSON
	if len(dict_vacancy) > 0:
		with open(name_file, "w", encoding='utf-8') as file:
			dict_old.update(dict_vacancy)
			json.dump(dict_old, file, indent=4, ensure_ascii=False)
	return dict_vacancy


def get_answer(lang, grade) ->list:
	answer = []
	if check_correct_data(lang, grade) == True:
		dict_vacancy = get_data_of_vacancy(lang, grade)
		if len(dict_vacancy) == 0:
			answer.append(answer_no_vacancy + host_name)
		else:
			for value in dict_vacancy.values():
				answer.append(str(value['title']) + " " \
					+ str(value['link']) + " " \
					+ " ".join([x for x in value['keys']]) + \
						" Опубликовано в " + str(value['time_pub']))
	else:
		answer.append(answer_wrong + host_name)
		answer.append(answer_list_cmd)
	return answer

	
if __name__ == "__main__":
	lang = "python"
	grade = "junior"
	msg = get_answer(lang, grade)
	print(msg)
