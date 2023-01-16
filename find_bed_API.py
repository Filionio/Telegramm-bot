
import requests
import json
def find_rapid(filter_user):
	"""Функция получает фильтр от пользователя ввиде списка и подставляет значения в поиск по сайту AirBnb.ru"""
	# filter_user - [0-город, 1- дата заезда, 2- дата выезда, 3-кол-во человек, 4- кол-во предложений]
	url = "https://airbnb13.p.rapidapi.com/search-location"

	querystring = {"location":"Berlin","checkin":"2023-09-10","checkout":"2023-10-11","adults":"1","children":"0","infants":"0","page":"1"}
	querystring["location"] = filter_user[0]
	querystring["checkin"] = filter_user[1]
	querystring["checkout"] = filter_user[2]
	querystring["adults"] = filter_user[3]
	querystring["page"] = filter_user[4]
	headers = {
		"X-RapidAPI-Key": "cc8187fcbfmsha5c244a3402267bp1d949cjsn6b73cec4391f",
		"X-RapidAPI-Host": "airbnb13.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	return pages(data,filter_user[4])

def pages(data,pages):
	'''Функция получает ссылки и картинки номеров гостиниц из API сайта
	и возвращает их в функцию find_rapid в виде генератора'''
	for page in range(int(pages)):
		yield data['results'][page]['url'], data['results'][page]['images'][1:3]

