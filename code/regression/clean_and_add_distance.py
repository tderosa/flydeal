# import googlemaps
import csv
import urllib2
import json
from datetime import date


distance_cache = {}

result_list = []
indices = [3, 8]
count = 1


# STORE THE WEEK PRICE IN THE MEMORY
week_price = {}
with open('../../data/outputs/week_price.csv', 'rb') as f:
	reader = csv.reader(f)
	next(reader, None)
	for row in reader:
		week = int(row[0])
		price = float(row[1])
		if not week in week_price:
			week_price[week] = price
		else:
			week_price[week].append(price)


# FOR EVERY FLIGHT DATA, NEED TO FIND THE DISTANCE DATA FROM distance24.org API AND ADD IT TO THE DATASET
# RETURNS THE DATA FOR LINEAR REGRESSION

with open('../../data/outputs/clean_price_data.csv', 'rb') as f:
	reader = csv.reader(f)
	next(reader, None)
	for row in reader: 

		from_loc = row[5] + '-' + row[7]
		to_loc = row[0] + '-' + row[4]
		url = 'http://www.distance24.org/route.json?stops='+ from_loc + '|' + to_loc

		from_to = (from_loc, to_loc)

		distance = 0
		if from_to in distance_cache:
			distance = distance_cache.get(from_to)
		else:
			try:
				content = json.loads(urllib2.urlopen(url).read())
				distance = content.get('distances')[0]
			except Exception, e:
				distance_cache[from_to] = None
				print 'distance not get'
				pass
			else:
				distance_cache[from_to] = distance

		price = row[3]
		duration = row[8]
		departure_time = int(row[9])
		num_of_week = date.fromtimestamp(departure_time).isocalendar()[1]
		week_score = int(week_price[num_of_week])

		index_h = duration.index('h')
		index_m = duration.index('m')
		duration = int(duration[:index_h]) * 60 + int(duration[index_h+1: index_m])

		if distance:
			result_list.append([duration, distance, week_score, price])
			print str(from_to) + '[WRITE] DISTANCE: ' + str(distance) + ' ---- ' + str(count)
			count += 1


with open('regressions.csv', 'wb') as fw:
	writer = csv.writer(fw)
	writer.writerow(['duration', 'distance', 'week score', 'price'])
	writer.writerows(result_list)


