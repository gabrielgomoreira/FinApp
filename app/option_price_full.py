import pandas as pd 
import json
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
n_period = 7
rate = 0.08
div = 0
h_period = 0
vol = 0.433764

def get_inputs():
	global call, american, ticker, t_time, h_period, stock_price, k_strike, vol

	temp_input = input('Call or Put?: ').upper()
	call = temp_input in ['CALL', 'C', '1']
	temp_input = input('American or European?: ').upper()
	american = temp_input in ['AMERICAN', 'AMER', 'A' '1']
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

def convert_parameters(inputs_from_user):
	global call, american, ticker, t_time, h_period, stock_price, k_strike, vol, n_period, div, rate
	print('inside of convert_parameters')
	print(inputs_from_user)
	american = inputs_from_user['american'].upper() in ['AMERICAN', 'AMER', 'A', '1']
	call = inputs_from_user['call'].upper() in ['CALL', 'C', '1']
	ticker = inputs_from_user['ticker'].upper()
	t_time = float(inputs_from_user['t_time'])
	k_strike = float(inputs_from_user['k_strike'])

	n_period = 3 if not inputs_from_user['n_period'] else int(inputs_from_user['n_period'] )
	rate = 0.03 if not inputs_from_user['rate'] else float(inputs_from_user['rate'] )
	div = 0 if not inputs_from_user['div'] else float(inputs_from_user['div'] )


	return_params = {'american':american, 'call':call, 'ticker':ticker, 'k_strike':k_strike, 't_time':t_time, 
						'rate':rate, 'n_period':n_period, 'div':div}

	return return_params


def get_values():
	series_data = get_inputs()
	option_object = Option(american=american,call=call, ticker=ticker, stock_price=stock_price, 
					k_strike=k_strike, t_time=t_time, vol=vol, rate=rate, n_period=n_period, div=div)
	
	black_scholes_price = option_object.get_black_scholes_price()
	print('Black Scholes Price %f ' %black_scholes_price)

	binomial_model_price = option_object.get_binomial_model_price()
	print('Binomial Model  Scholes Price %f ' %binomial_model_price)
	opposite_opt_prices = option_object.get_from_put_call_parity()
	print('Put-Call Parity: %s' % opposite_opt_prices)
	print('Rand Vars and Prob: %s' % option_object.get_prob_from_zscore())
	option_object.graph_sprobabilities_bm()

def get_data_set_name(database, dataset):
	with open('../db_scripts/database_and_dataset_names.json') as json_file:
		dataset_names = json.load(json_file)
		if database in dataset_names and dataset in dataset_names[database]:
			return dataset_names[database][dataset]['name']
		else:
			return 'ERROR: Name not found'


def calculate_opt_prices(option_parameters):
	
	series_data = get_pandas_series('WIKI', option_parameters['ticker'])
	stock_name = get_data_set_name('WIKI', option_parameters['ticker'])
	stock_price = series_data.tail(1)[-1]
	amount_days = int((t_time*252))
	
	vol = get_vol_from_pandas(series_data, vol_horizon=amount_days, avg=1)

	option_parameters['stock_price'] = stock_price
	option_parameters['vol'] = vol
	option_parameters['stock_name'] = stock_name

	option_object = Option(**option_parameters)


	black_scholes_price = option_object.get_black_scholes_price()
	binomial_model_price = option_object.get_binomial_model_price()

	opposite_opt_prices = option_object.get_from_put_call_parity()
	opposite_black_scholes_price = opposite_opt_prices['black_scholes_price']
	opposite_binomial_model_price = opposite_opt_prices['binomial_model_price']

	rand_vars = option_object.get_prob_from_zscore()
	mean = rand_vars['mean']
	prob = rand_vars['prob']
	stdev = rand_vars['stdev']
	opt_type = 'American' if american else 'European'
	opt_name = 'Call' if call else 'Put'
	opt_inv_name = 'Put' if call else 'Call'

	return {'stock_name':stock_name, 'stock_price':stock_price, 'vol':vol, 'series_data': series_data, 'black_scholes_price': black_scholes_price, 
			'binomial_model_price': binomial_model_price, 'opposite_black_scholes_price': opposite_black_scholes_price,
			'opposite_binomial_model_price': opposite_binomial_model_price,	'opt_name': opt_name, 'opt_inv_name': opt_inv_name,
			'mean': mean, 'prob': prob, 'stdev': stdev, 'opt_type':opt_type}



# get_values()