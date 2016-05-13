import csv
import numpy as np
from datetime import date


results = {}

# CALCULATE THE POPULARITY OF THE WEEK BY CALCULATING THE AVERAGE FLIGHT PRICE OF THAT WEEK
with open('../../data/outputs/clean_price_data.csv', 'rb') as f:
	reader = csv.reader(f)
	next(reader, None)
	for row in reader: 
		price = float(row[3])
		departure_time = int(row[9])
		num_of_week = date.fromtimestamp(departure_time).isocalendar()[1]
		if not num_of_week in results:
			results[num_of_week] = [price]
		else:
			results[num_of_week].append(price)

# WRITE THE WEEK SCORE TO FILE
	with open('../../data/outputs/week_price.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['num_of_week', 'price'])
		for key, val in results.items():
			mean = np.mean(val)
			writer.writerow([key, mean])



	# with open('regression_test_week.csv', 'wb') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(['week', 'price'])
	# 	writer.writerows(results)