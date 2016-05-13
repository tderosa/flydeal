import json
from urllib2 import urlopen
import time
from datetime import datetime

# SCRAP FROM SKYPICKER

URL = 'https://api.skypicker.com/flights?flyFrom=BOS&dateFrom=10/6/2016&dateTo=12/6/2016&typeFlight=oneway&directFlights=1'
START_DATE = datetime.today()
SECS_PER_DAY = 86400
DAYS_PER_YEAR = 365
FROM = ['BOS', 'LAX', 'PHL', 'ATL', 'ORD', 'DFW', 'JFK', 'SFO', 'DEN', 'LAS']



def generate_url(date_str, dest_str):
	return 'https://api.skypicker.com/flights?flyFrom=' + dest_str + '&dateFrom=' + str(date_str) + '&dateTo=' + str(date_str) + '&typeFlight=oneway&directFlights=1'


def get_list():

	# starting from April 1st 2016 to April 1st 2017
	

	content_list = []

	for dest_str in FROM:
		posix = time.mktime(START_DATE.timetuple())

		for day in range(DAYS_PER_YEAR):
			print 'Day ' + str(day)
			posix += 86400
			utc_date = datetime.utcfromtimestamp(posix)
			date_str = utc_date.strftime("%d/%m/%Y")
			url = generate_url(date_str, dest_str)
			# print url
			content_list += json.loads(urlopen(url).read()).get('data')

	return content_list


# CLEAN THE DATA

def formulate_json(data_list):
	cleaned_list = []
	for data in data_list:
		route = data['route'][0]
		cleaned_data = {
			'airline': route['airline'],
			'flight_no': route['flight_no'],
			'price': data['price'],
			'from_city': data['mapIdfrom'],
			'to_city': data['mapIdto'],
			'from_airport': data['flyFrom'],
			'to_airport': data['flyTo'],
			'departure_time': data['dTimeUTC'],
			'arrive_time': data['aTimeUTC'],
			'duration': data['fly_duration'],		
		}

		cleaned_list.append(cleaned_data)

	return json.dumps({'data': cleaned_list})



# WRITE TO FILES

def main():

	print 'start scraping...'
	flight_list = get_list()
	# print len(flight_list)
	cleaned_data = formulate_json(flight_list)

	with open('../../data/flight_data_big.json', 'w') as f:
		f.write(cleaned_data)

	print 'done!'




if __name__ == '__main__':
	main()