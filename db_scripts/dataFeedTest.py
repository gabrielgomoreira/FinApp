import requests, datetime, json
from pprint import pprint

# Get Apple's stock prices during November 2012 sorted in ascending order excluding column names.  Include only column 4 (closing price) and collapse the frequency to weekly while returning per cent changes.
# curl "https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?order=asc&exclude_column_names=true&start_date=2012-11-01&end_date=2012-11-30&column_index=4&collapse=weekly&transformation=rdiff


with open('../sp500companies.json') as data_file:
	companies = json.load(data_file)
	for comp in companies:
		ticker = comp['Symbol']
		src = "https://www.quandl.com/api/v3/datasets/WIKI/"+ticker+".json?api_key=eycsYzhTMri1cwHabVMs"
		src_request = requests.get(src).json()			
		# data = json.loads(json.dumps(arrests))
		with open(ticker+'.json', 'w') as outfile:
			json.dump(src_request, outfile)