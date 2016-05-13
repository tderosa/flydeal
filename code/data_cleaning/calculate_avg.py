import csv
import json
from collections import defaultdict
import datetime

weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
csvName = ""

def getWeekday(stamp):
	return int(datetime.datetime.fromtimestamp(int(stamp)).weekday())

def getTime(stamp):
	return datetime.datetime.fromtimestamp(int(stamp)).time()


def main():
	with open(csvName, "rU") as csvFlights:
		
		reader = csv.reader(csvFlights)
		headers = reader.next()
		price_idx = headers.index("price")
		airline_idx = headers.index("airline name")
		flight_num_idx = headers.index("flight number")
		departure_idx = headers.index("departure time")
		equipment_desc_idx = headers.index("equipment desc")
		on_time_idx = headers.index("on time percentage")
		distance_idx = headers.index("distance")
		duration_idx = headers.index("duration")
		meal_idx = headers.index("meal")
		departure_city_idx = headers.index("departure city")
		arrival_city_idx = headers.index("arrival city")
		departure_airport_code_idx = headers.index("departure airport")
		arrival_airport_code_idx = headers.index("arrival airport")

		prices = defaultdict(list)
		durations = defaultdict(list)
		weekdays = defaultdict(list)
		meals = defaultdict(lambda: defaultdict(int))
		equipments = defaultdict(lambda: defaultdict(int))
		on_times = defaultdict(list)

		departures = defaultdict(lambda: defaultdict(int))

		arrival_times = defaultdict(lambda: defaultdict(int))
		departure_times = defaultdict(lambda: defaultdict(int))

		for flight in reader:
			flight_id = str(flight[airline_idx]) + "_" + str(flight[flight_num_idx]) + "_" + str(flight[departure_city_idx]) + "_" + str(flight[departure_airport_code_idx]) + "_" + str(flight[arrival_city_idx]) + "_" + str(flight[arrival_airport_code_idx])

			prices[flight_id].append(float(flight[price_idx]))
			durations[flight_id].append(int(flight[duration_idx]))
			departures[flight_id][getWeekday(flight[departure_idx])] += 1
			departure_times[flight_id][getTime(flight[departure_idx])] += 1
			meals[flight_id][flight[meal_idx]] += 1
			equipments[flight_id][flight[equipment_desc_idx]] += 1
			if flight[on_time_idx]:
				on_times[flight_id].append(int(flight[on_time_idx]))


		headers = ["flight_no", "airline", "duration", "price", 
					"most_common_depart_day", 
					"most_common_depart_time", "most_common_meal", "most_common_equipment", "avg_on_time",
					"departure airport", "departure city", "arrival airport", "arrival city"]
		
		with open("averages.csv", 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(headers)

			for key in prices.keys():
				key_split = key.split("_")

				flight_no = key_split[1]
				airline = key_split[0]

				departure_city = key_split[2]
				arrival_city = key_split[3]
				departure_airport_code = key_split[4]
				arrival_airport_code = key_split[5]

				
				p = prices[key]
				d = durations[key]
				t = on_times[key]
				duration = sum(d)/len(d)
				price = sum(p)/len(p)

				avg_on_time = -1
				if len(t) > 0:
					avg_on_time = sum(t)/len(t)

				most_common_depart_day = -1
				max_occurrences_depart_day = -1

				for i in range(7):
					day = i
					if departures[key][day] > max_occurrences_depart_day:
						max_occurrences_depart_day = departures[key][day]
						most_common_depart_day = day


				most_common_depart_time = -1
				max_occurrences_depart_time = -1

				for time in departure_times[key].keys():
					if departure_times[key][time] > max_occurrences_depart_time:
						max_occurrences_depart_time = departure_times[key][time]
						most_common_depart_time = time


				most_common_equipment = -1
				max_occurrences_equip = -1

				for equip in equipments[key].keys():
					if equipments[key][equip] > max_occurrences_equip:
						max_occurrences_equip = equipments[key][equip]
						most_common_equipment = equip


				most_common_meal = -1
				max_occurrences_meal = -1

				for meal in meals[key].keys():
					if meals[key][meal] > max_occurrences_meal:
						max_occurrences_meal = equipments[key][meal]
						most_common_meal = meal


				row = [flight_no, airline, duration, price, 
						weekday_names[most_common_depart_day], 
						most_common_depart_time, most_common_meal, most_common_equipment, avg_on_time,
						departure_city, arrival_city, departure_airport_code, arrival_airport_code]

				writer.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: python calculate_price_average.py flight_price_unclean_data'
    csvName = sys.argv[1]
    main()



