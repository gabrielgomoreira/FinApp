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
n_period = 25
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


"""
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
Black Scholes Pirce 39.581683 
: 50.09687943007085, 2: 36.542582435749878, 3: 43.063509629441164, 4: 38.37619403881363, 5: 41.6097982184776, 6: 38.965803280411421, 7: 40.989017717552905, 8: 39.239476986143458, 9: 40.645594832026291, 10: 39.390892424824294, 11: 40.427776498752642, 12: 39.483763603290079, 13: 40.277361562835239, 14: 39.544690156886908, 15: 40.167275007556938, 16: 39.586571101890705, 17: 40.083223358182472, 18: 39.616344758887799, 19: 40.016951388841427, 20: 39.638038990961434, 21: 39.963359189711561, 22: 39.654133094308378, 23: 39.919126544988281, 24: 39.6662256646202, 25: 39.881999098174994}

"""