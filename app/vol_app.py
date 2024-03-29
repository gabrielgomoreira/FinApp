import requests, datetime, json
import pandas as pd
import numpy as np
import datetime as dt
import Quandl
import matplotlib.pyplot as plt
from pprint import pprint
from matplotlib import style
from statistics import mean

# plt.plot([1,2,3,4])

# api_key = open('quandlapikey.txt','r').read()

# df = Quandl.get("FMAC/HPI_TX", authtoken=api_key)

# print(df.head())


# Get Apple's stock prices during November 2012 sodaily_log_retsed in ascending order excluding column names.  Include only column 4 (closing price) and collapse the frequency to weekly while returning per cent changes.
# curl "https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?order=asc&exclude_column_names=true&stadaily_log_rets_date=2012-11-01&end_date=2012-11-30&column_index=4&collapse=weekly&transformation=rdiff
horizon = 252

def window_vol_list(window, daily_log_rets, hor_sqr):

	vol_list = []

	for d in range(window, len(daily_log_rets)):
		vol_list += [np.std(daily_log_rets[(d-(window)):d]) * 100 * hor_sqr]
	return vol_list

def get_vix():
	vix_plot = []

	with open('../db_scripts/sp500companiesFolder/VXST.json') as vix_file:
		vix = json.load(vix_file)['dataset']
		day = 0
		for d in vix['data']:
			if(day > horizon):
				break
			else:
				vix_plot += [d[4]]
				day += 1

	return vix_plot

def get_adjclose_dates(df):
	close_price = []
	dates = []

	day = 0
	for d in df['data']:
		if(day > horizon):
			break
		else:
			dates += [d[0]]
			close_price += [d[11]] # adjusted close
			day += 1

	vix_plot = get_vix()

	x_axis = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

	name = df['name'].split('Prices,')[0]
	return {'Dates':x_axis, 'Adjusted_Close': close_price, 'Name':name, 'VIX':vix_plot}

def plot_vol_graph(vol_lists, vol_horizon, date_and_close):
	comp_name = date_and_close['Name']
	vix = date_and_close['VIX']
	dates = date_and_close['Dates']

	for vol_lt in vol_lists:
		label_name = "Window: " + str(horizon-len(vol_lt))
		# print(len(dates) == len(vol_lt))
		plt.plot(vol_lt, label=label_name)


	plt.plot(vix, label='VIX', linewidth=2.0, color='r')
	# plt.plot(sp0[6:], label='wok plz')
	plt.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0)
	plt.title(comp_name)

	plt.show()

def calculate_vol(ticker):
	ticker = ticker.upper()
	hor_sqr = np.sqrt(horizon)

	company_json = '../db_scripts/sp500companiesFolder/'+ticker+'.json'
	df = pd.read_json(company_json)['dataset']

	date_and_close = get_adjclose_dates(df)

	sp0 = date_and_close['Adjusted_Close']
	zip_sp = zip(sp0[1:],sp0)
	#logarithimic price changes

	log_diff = lambda d2, d1: np.log(d2/d1)
	daily_log_rets = [log_diff(d2,d1) for d2, d1 in zip_sp]
	avg_stdev_daily_vol = np.std(daily_log_rets)
	vol_horizon = hor_sqr * avg_stdev_daily_vol * 100

	vol_lists = []
	size = len(daily_log_rets)
	for window in range(2, 5):
		if(size % window == 0):
			# print(window)
			vol_lists += [window_vol_list(window,daily_log_rets,hor_sqr)]

	# print(vol_lists)	
	# plot_vol_graph(vol_lists, vol_horizon, date_and_close)

	return vol_horizon

def get_vol_from_pandas(series, vol_horizon=252, avg=1):
	rows_needed = vol_horizon + avg
	data_to_use = series.tail(rows_needed)

	zip_data = zip(data_to_use[1:], data_to_use)
	log_diff = lambda t_1, t_0: np.log(t_1/t_0)
	daily_log_rets = [log_diff(d2,d1) for d2, d1 in zip_data]
	avg_stdev_daily_vol = np.std(daily_log_rets) * (vol_horizon**0.5)
	return avg_stdev_daily_vol





	# daily_log_rets = [log_diff(d2,d1) for d2, d1 in zip_sp]
	# avg_stdev_daily_vol = np.std(daily_log_rets)
	# vol_horizon = hor_sqr * avg_stdev_daily_vol




# plt.plot(x_axis, close_price)
# plt.ylabel('some numbers')
# plt.show()

# daily calculation

calculate_vol('FB')

