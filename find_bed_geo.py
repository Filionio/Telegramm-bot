import requests
import json

def find_geo(latitude,longitude,filter_user):
	url = "https://airbnb13.p.rapidapi.com/search-geo"
	querystring = {"ne_lat":"52.51","ne_lng":"13.41","sw_lat":"52.41","sw_lng":"13.51","checkin":"2022-05-15","checkout":"2022-05-16","adults":"1","children":"0","infants":"0","page":"1"}
	querystring["ne_lat"] = latitude + 1
	querystring["sw_lat"] = latitude - 1
	querystring["ne_lng"] = longitude + 1
	querystring["sw_lng"] = longitude - 1
	querystring['page'] = int(filter_user[0])
	querystring["checkin"] = filter_user[1]
	querystring["checkout"] = filter_user[2]
	headers = {
		"X-RapidAPI-Key": "d84165b781msh290cf99c394ad2dp19236ajsn6b54eeb5c463",
		"X-RapidAPI-Host": "airbnb13.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	return pages(data,filter_user[0])

def pages(data,total_pages):
	links = []
	images = []
	for page in range(int(total_pages)):
		links.append(data['results'][page]['url'])
		images.append(data['results'][page]['images'][1:3])
	return links,images