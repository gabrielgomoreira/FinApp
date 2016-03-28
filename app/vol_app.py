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


# Get Apple's stock prices during November 2012 sorted in ascending order excluding column names.  Include only column 4 (closing price) and collapse the frequency to weekly while returning per cent changes.
# curl "https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?order=asc&exclude_column_names=true&start_date=2012-11-01&end_date=2012-11-30&column_index=4&collapse=weekly&transformation=rdiff


df = pd.read_json('../db_scripts/sp500companiesFolder/FB.json')['dataset']

close_price = []
dates = []
for d in reversed(df['data']):
	dates += [d[0]]
	close_price += [d[11]]


x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

plt.plot(x, close_price)
plt.ylabel('some numbers')
plt.show()

