# flydeal
CS1951a Final Project -- ajb7, kb25, tderosa, ybao1

ybao1
  Regression Analysis and Data Scraping Instruction

	DATA SCRAPING:
	1. python scrap_skypicker.py - It scraps the data from Skypicker API and save to flight_data_big.json in data/
	2. python scrap_clean_domestic.py - It scraps and clean the data from Expedia API and save to clean_domestic_flight.csv in data/outputs/

	DATA CLEANING:
	3. python week_average.py - It calculate the week popularity score and write the scores to week_price.csv in data/outputs/, it depends on data/outputs/clean_price_data.csv
	4. python clean_and_add_distance.py - It combines the existing flight data (data/outputs/clean_price_data.csv) and the distance data scraped from distance24.org together to form the dataset for linear regression analysis. It produces regressions.csv in data/outputs, and it depends on week_price.csv and clean_price_data.csv in data/outputs

	REGRESSIONS
	5. python linear_regression.py - It runs multiple linear regression on the regressions.csv in data/outputs. it prints out the score and I commented out K-fold cross validation. It also defines the error tickets based on the result of the predictions and categorized the existing dataset into a new dataset for the logistic regression analysis on error tickets and save the dataset to logreg.csv in data/outputs/. Finally it also plots the linear relation between price and duration, and price and distance
	6. python regressions.py - It runs logistic regression on the logreg.csv in data/outputs to predict whether the ticket is an error ticket. I commented out K-fold cross validation and other classifiers like linear SVC, Naive Bayes etc... It produces the scatterplot of the error tickets vs duration and distance.