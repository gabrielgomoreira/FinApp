import pandas as pd 
from get_data import get_pandas_series
from vol_app import get_vol_from_pandas
from black_scholes_model import Black_Scholes
from option import Option


american = False
call = True
ticker = 'TSLA'
t_time = 1

stock_price = 250.07
k_strike = 280
n_period = 1
rate = 0.08
div = 0
h_period = 0
vol = 0.433764

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
	option_object = Option(american=american,call=call, ticker=ticker, stock_price=stock_price, 
					k_strike=k_strike, t_time=t_time, vol=vol, rate=rate, n_period=n_period, div=div)
	
	black_scholes_price = option_object.get_black_scholes_price()
	print('Black Scholes Pirce %f ' %black_scholes_price)

	binomial_model_price = option_object.get_binomial_model_price()
	opposite_opt_prices = option_object.get_from_put_call_parity()
	print('Put-Call Parity: %s' % opposite_opt_prices)
	print('Rand Vars and Prob: %s' % option_object.get_prob_from_zscore())
	option_object.graph_sprobabilities_bm()



get_values()