from urllib2 import urlopen
import json
import time
import csv
import re
from datetime import datetime, date

API_KEY = 'WXBYVAZYbBQDwuBpdmhvYf23YtD5UaWj'

TO = ['MIA', 'MCO', 'ATL', 'LAX', 'PHL', 'ORD', 'DFW', 'DEN', 'SFO']
FROM = 'BOS'

START_DATE = datetime.today()
SECS_PER_DAY = 86400
DAYS_PER_YEAR = 270

def generate_url(date_str, from_airport, to_airport):
	return 'http://terminal2.expedia.com/x/mflights/search?departureAirport=' + from_airport + '&arrivalAirport='+ to_airport +'&departureDate=' + str(date_str) + '&apikey=' + API_KEY


def get_list():

	try:
		leg_list = []
		offer_list = []

		for to_airport in TO:
			posix = time.mktime(START_DATE.timetuple())

			for day in range(DAYS_PER_YEAR):
				print ('Day ' + str(day) + ' --- ' + to_airport)
				posix += 86400
				utc_date = datetime.utcfromtimestamp(posix)
				date_str = utc_date.strftime("%Y-%m-%d")
				url = generate_url(date_str, FROM, to_airport)

				# scrap
				try:
					content = urlopen(url).read()
					index = content.index('{')
				except Exception, e:
					print ('url error')
					pass

				try:
					if index:
						data = json.loads(content[index:])
					else:
						data = json.loads(content)

					leg_list += data.get('legs')
					offer_list += data.get('offers')
				except Exception, e:
					print ('Ah!')
					pass
	except Exception, e:
		pass

	return (leg_list, offer_list)


# CLEAN AND RETURN THE DOMESTIC FLIGHT DATA

def formulate_all(data_tuple):
	result_list = []
	legs = data_tuple[0]
	offers = data_tuple[1]

	prices = {}
	for offer in offers:
		id = offer.get('legIds')[0]
		price = offer.get('totalFare')
		if not id in prices:
			prices[id] = price

	for leg in legs:
		id = leg.get('legId')
		try:
			seg = leg.get('segments')[0]
			price = prices.get(id)
			departure_time = int(seg.get('departureTimeEpochSeconds'))
			airline_name = seg.get('airlineName')
			flight_number = seg.get('flightNumber')
			equipment_code = seg.get('equipmentCode')
			equipment_desc = seg.get('equipmentDescription')
			arrival_airport = seg.get('arrivalAirportCode')
			arrival_city = seg.get('arrivalAirportLocation')
			departure_airport = seg.get('departureAirportCode')
			departure_city = seg.get('departureAirportLocation')
			on_time_percentage = seg.get('onTimePercentage')
			distance = seg.get('distance')
			duration = seg.get('duration')
			# clean duration
			pattern = r'PT(\d+H)*(\d+M)*'
			prog = re.compile(pattern)
			m = prog.search(duration)
			if m.group(1) and m.group(2):
				duration = int(m.group(1)[:-1]) * 60 + int(m.group(2)[:-1])
			else:
				if m.group(1):
					duration = int(m.group(1)[:-1]) * 60
				else:
					duration = int(m.group(2)[:-1])
			meal = seg.get('meal')

		except Exception, e:
			print ('Ahh')
			pass
		result_list.append([price, airline_name, flight_number, departure_airport, departure_city, arrival_airport, arrival_city, departure_time, equipment_code, equipment_desc, on_time_percentage, distance, duration, meal])

	return result_list	


def formulate_decision(data_tuple):
	result_list = []
	legs = data_tuple[0]
	offers = data_tuple[1]

	prices = {}
	for offer in offers:
		id = offer.get('legIds')[0]
		price = offer.get('totalFare')
		if not id in prices:
			prices[id] = price

	for leg in legs:
		id = leg.get('legId')
		try:
			seg = leg.get('segments')[0]
			price = prices.get(id)
			departure_time = int(seg.get('departureTimeEpochSeconds'))
			num_of_week = date.fromtimestamp(departure_time).isocalendar()[1]
			result_list.append([price, num_of_week])

		except Exception, e:
			print ('Ahh')
			pass

	return result_list

def formulate_lin_decision(data_tuple):
	result_list = []
	legs = data_tuple[0]
	offers = data_tuple[1]

	prices = {}
	for offer in offers:
		id = offer.get('legIds')[0]
		price = offer.get('totalFare')
		if not id in prices:
			prices[id] = price

	for leg in legs:
		id = leg.get('legId')
		try:
			seg = leg.get('segments')[0]
			price = prices.get(id)
			departure_time = int(seg.get('departureTimeEpochSeconds'))
			num_of_week = date.fromtimestamp(departure_time).isocalendar()[1]
			result_list.append([price, num_of_week])

		except Exception, e:
			print ('Ahh')
			pass

	return result_list



def formulate_regression(data_tuple):
	result_list = []
	legs = data_tuple[0]
	offers = data_tuple[1]

	prices = {}
	for offer in offers:
		id = offer.get('legIds')[0]
		price = offer.get('totalFare')
		if not id in prices:
			prices[id] = price

	for leg in legs:
		id = leg.get('legId')
		try:
			seg = leg.get('segments')[0]
			price = prices.get(id)
			on_time_percentage = seg.get('onTimePercentage')
			distance = seg.get('distance')
			duration = seg.get('duration')
			print (duration)
			# clean duration
			pattern = r'PT(\d+H)*(\d+M)*'
			prog = re.compile(pattern)
			m = prog.search(duration)
			if m.group(1) and m.group(2):
				duration = int(m.group(1)[:-1]) * 60 + int(m.group(2)[:-1])
			else:
				if m.group(1):
					duration = int(m.group(1)[:-1]) * 60
				else:
					duration = int(m.group(2)[:-1])

			if on_time_percentage:
				result_list.append([price, duration, distance, on_time_percentage])
		except Exception, e:
			print ('Ah')
			pass

	return result_list


# WRITE THE CLEANED DOMESTIC DATA

def main():
	print ('start scraping...')
	flight_list = get_list()

	cleaned_data = formulate_all(flight_list)
	print (cleaned_data)

	with open('../../data/outputs/clean_domestic_flight.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['price', 'airline name', 'flight number', 'departure airport', 'departure city', 'arrival airport', 'arrival city', 'departure time', 'equipment code', 'equipment desc', 'on time percentage', 'distance', 'duration', 'meal'])
		writer.writerows(cleaned_data)
	print ('done!')


if __name__ == '__main__':
	main()