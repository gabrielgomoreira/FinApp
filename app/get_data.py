import Quandl
import matplotlib.pyplot as plt
from vol_app import get_vol_from_pandas

api_key = open('../quandl_api_key.txt', 'r').read()


"""
DATABASE: WIKI, CBOE,...
"""
def get_pandas_series(database, dataset):
	database = database.upper()
	dataset = dataset.upper()
	data_to_get = database+"/"+dataset
	
	series_data = Quandl.get(data_to_get, authtoken=api_key)
	column_names = list(series_data.columns.values)
	close = [col for col in column_names if 'CLOSE' in col.upper()][-1]

	series_close = series_data[close]
	series_close.name = data_to_get

	return series_close

def setup():
	database = 'WIKI'
	dataset = 'S'
	series_data = get_pandas_series(database, dataset)
	vol_horizon = 252
	avg = 0
	get_vol_from_pandas(series_data, vol_horizon=vol_horizon, avg=avg)



setup()