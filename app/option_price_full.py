import pandas as pd 
from get_data import get_pandas_series
from vol_app import get_vol_from_pandas
from black_scholes_model import Black_Scholes
from option import Option


american = False
call = False
ticker = 'GS'
t_time = 1

stock_price = 41
k_strike = 40
n_period = 3
rate = 0.08
div = 0
h_period = 0
vol = 0.3

def get_inputs():
	global call, american, ticker, t_time, h_period, stock_price, k_strike, vol

	temp_input = input('Call or Put?: ').upper()
	call = temp_input in ['CALL', 'C', '1']
	temp_input = input('American or European?: ').upper()
	american = temp_input in ['AMERICAN', 'AMER' '1']
	ticker = input('Enter Ticker Symbol: ').upper()
	t_time = float(input('Enter lenght (float) of time (in years) for option: '))
	h_period= (t_time/n_period)
	series_data = get_pandas_series('WIKI', ticker)
	stock_price = series_data.tail(1)[-1]
	amount_days = int((t_time*252))
	vol = get_vol_from_pandas(series_data, vol_horizon=amount_days, avg=1)
	print('%s\'s last close price is: %.2f\nFor the past %d days it\'s realized volatility is: %f'
			%(ticker, stock_price, amount_days, vol))
	k_strike = float(input('Enter K strike price (float) for your option: '))

	return series_data
def get_values():
	# series_data = get_inputs()
	# black_scholes_opt = Black_Scholes(call=call, stock_price=stock_price, 
	# 									k_strike=k_strike, t_time=t_time,
	# 									vol=vol, rate=rate, div=div)
	# bs_price = black_scholes_opt.get_option_price()
	option = Option(american=american,call=call, ticker=ticker, stock_price=stock_price, 
					k_strike=k_strike, t_time=t_time, vol=vol, rate=rate, n_period=n_period, div=div)
	print(option.get_binomial_model_price())




get_values()