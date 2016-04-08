import requests, datetime, json
import Quandl


api_key = open('../quandl_api_key.txt', 'r').read()

def get_stock(database, dataset):
	database = database.upper()
	dataset = dataset.upper()
	stock_data = Quandl.get(database+"/"+dataset, authtoken=api_key)
	print(type(stock_data))


get_stock('WIKI', 'S')

