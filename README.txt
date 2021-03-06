# flydeal
CS1951a Final Project -- ajb7, kb25, tderosa, ybao1

All Visualizations: http://tderosa.github.io/flydeal/

Delay Visualization can also be viewed by opening code/delay_viz/delay-viz.html
Price Visualization can also be viewed by opening code/price_viz/price-viz.html

DATA SCRAPING:
	1. python scrap_skypicker.py - Scrapes data from the Skypicker API and saves it to flight_data_big.json in data/
	2. python scrap_clean_domestic.py - Scrapes and cleans data from the Expedia API and saves it to clean_domestic_flight.csv in data/outputs/

DATA CLEANING:
	3. python price_delay_clean1.py flight_data to_clean_dir_path output_dir_path overwrite?<0/1> - Step one of price and delay cleaning and aggregating. Reads in flight and delay data, finds matches, and calculates averages and max delays for all flights with price data. The overwrite flag specifies whether to restart the output files or add to those that already exist.
	4. python price_delay_clean2.py price_delay_init mon_year_init dow_init time_init airport_loc output_dir - Step two of price and delay cleaning and aggregating. Reads in the outputs of step one and calculates overall averages and max delays for each flight with pricing data. Outputs to clean_price_data.csv, dow_delays.csv, mon_year_delays.csv, and time_delays.csv.
	5. python week_average.py - Calculates the week popularity score and writes the scores to week_price.csv in data/outputs/, depends on data/outputs/clean_price_data.csv
	6. python clean_and_add_distance.py - Combines the existing flight data (data/outputs/clean_price_data.csv) and the distance data scraped from distance24.org together to form the dataset for linear regression analysis. It produces regressions.csv in data/outputs, and depends on week_price.csv and clean_price_data.csv in data/outputs
	7. python calculate_avg.py [flight_price_unclean_data.csv] - Calculates the average or most common value (when applicable) from data in the format of data/outputs/unclean_flight_price.csv and using (Airline, Flight #) pairs as the unique identifier computes averages for each airline's various flight routes, then saves these averages to data/outputs/cleaned_flight_averages.csv.

REGRESSIONS
	8. python linear_regression.py - Runs multiple linear regression on the regressions.csv in data/outputs. It prints out the score, but I commented out K-fold cross validation. It also defines the error tickets based on the result of the predictions and categorized the existing dataset into a new dataset for the logistic regression analysis on error tickets and saves the dataset to logreg.csv in data/outputs/. Finally, it plots the linear relation between price and duration, and price and distance.
	9. python regressions.py - Runs logistic regression on the logreg.csv in data/outputs to predict whether the ticket is an error ticket. I commented out K-fold cross validation and other classifiers like linear SVC, Naive Bayes etc... It produces the scatterplot of the error tickets vs duration and distance. 