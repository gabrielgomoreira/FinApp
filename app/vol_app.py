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

def window_vol_list(window, daily_log_rets, hor_sqr):

	vol_list = []
	print(len(daily_log_rets))
	for d in range(window-1, len(daily_log_rets)):
		vol_list += [np.std(daily_log_rets[(d-(window-1)):d]) * 100 * hor_sqr]
	return vol_list


def func():
	df = pd.read_json('../db_scripts/sp500companiesFolder/FB.json')['dataset']
	horizon = 252
	hor_sqr = np.sqrt(horizon)
	# window = 7

	close_price = []
	dates = []
	for d in reversed(df['data']):
		dates += [d[0]]
		close_price += [d[11]]


	x_axis = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

	sp0 = close_price[-(horizon+1):]
	zip_sp = zip(sp0[1:],sp0)

	#logarithimic price changes
	log_diff = lambda d2, d1: np.log(d2/d1)
	daily_log_rets = [log_diff(d2,d1) for d2, d1 in zip_sp]
	avg_stdev_daily_vol = np.std(daily_log_rets)
	annualized_vol = hor_sqr * avg_stdev_daily_vol * 100

	vol_lists = []
	size = len(daily_log_rets)
	for window in range(2, 24):
		if(size % window == 0):
			vol_lists += [window_vol_list(window,daily_log_rets,hor_sqr)]
	window_vol_list(window,daily_log_rets,hor_sqr)

	print('Annualized vol: %f' % annualized_vol)
	for vol_lt in vol_lists:
		label_name = "Window: " + str(horizon-len(vol_lt))
		plt.plot(vol_lt, label=label_name)

	# plt.plot(sp0[6:], label='wok plz')
	plt.legend(bbox_to_anchor=(1.05, 1), loc=5, borderaxespad=0)
	plt.show()

# plt.plot(x_axis, close_price)
# plt.ylabel('some numbers')
# plt.show()

# daily calculation

func()

