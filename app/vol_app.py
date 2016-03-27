import requests, datetime, json
from pprint import pprint

import matplotlib.pyplot as plt
# plt.plot([1,2,3,4])



# Get Apple's stock prices during November 2012 sorted in ascending order excluding column names.  Include only column 4 (closing price) and collapse the frequency to weekly while returning per cent changes.
# curl "https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?order=asc&exclude_column_names=true&start_date=2012-11-01&end_date=2012-11-30&column_index=4&collapse=weekly&transformation=rdiff


with open('../db_scripts/sp500companiesFolder/FB.json') as data_file:
	companyJSON = json.load(data_file)
	data  = companyJSON['dataset']['data']
	cols = companyJSON['dataset']['column_names']
	close_price = []
	for d in reversed(data):
		close_price += [d[4]]

	plt.plot(close_price)
	plt.ylabel('some numbers')
	plt.show()