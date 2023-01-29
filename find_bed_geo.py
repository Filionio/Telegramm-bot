import requests
import json

def find_geo(latitude,longitude):
	url = "https://airbnb13.p.rapidapi.com/search-geo"
	querystring = {"ne_lat":"52.51","ne_lng":"13.41","sw_lat":"52.41","sw_lng":"13.51","checkin":"2022-05-15","checkout":"2022-05-16","adults":"1","children":"0","infants":"0","page":"1"}
	querystring["ne_lat"] = latitude + 1
	querystring["sw_lat"] = latitude - 1
	querystring["ne_lng"] = longitude + 1
	querystring["sw_lng"] = longitude - 1
	querystring["checkin"] = "2023-09-10"
	querystring["checkout"] = "2023-09-11"
	headers = {
		"X-RapidAPI-Key": "d84165b781msh290cf99c394ad2dp19236ajsn6b54eeb5c463",
		"X-RapidAPI-Host": "airbnb13.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	return pages(data)

def pages(data):
	for page in range(2):
		yield data['results'][page]['url'], data['results'][page]['images'][1:3]