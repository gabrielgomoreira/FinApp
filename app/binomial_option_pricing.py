#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import collections

american = True
call = True

stock_price = 41
k_strike = 40
rate = 0.08
div=0
t_time = 1
n_period = 20
h_period= (t_time/n_period)
vol = 0.3


def get_up_down():
	up = np.exp( ((rate-div)*h_period)   + (vol*np.sqrt(h_period))  )
	down = np.exp( ((rate-div)*h_period) - (vol*np.sqrt(h_period))  )
	return up, down

def get_risk_neutral_prob(up=0, down=0):
	return ((np.exp((rate-div)*h_period)-down)/(up-down))

def calculate_period_price(r_neutral_prob=0.5, opt_up=0, opt_down=0):
	price = ((opt_up*r_neutral_prob)+(opt_down*(1-r_neutral_prob)))
	pv = np.exp(-rate*h_period)
	return pv * price

def calculate_stock_prices(stock_price, up, down, n_period):
	s_price_tree = {0:[stock_price]}
	for period in range(1, n_period+1):
		sprices_for_period = []
		if(period == 1): # first istance
			sprices_for_period = [stock_price*up, stock_price*down]
		else:
			for i in range(0,len(s_price_tree[period-1]),2):
				su = s_price_tree[period-1][i]
				sd = s_price_tree[period-1][i+1]

				suu = su*up
				sud = su*down
				sdu = sd*up
				sdd = sd*down
				sprices_for_period += [suu,sud,sdu,sdd]
		
		s_price_tree[period] = sprices_for_period

	return s_price_tree

def calculate_option_from_tree(s_price_tree, r_neutral_prob, k_strike, call=True, american=True):
	opt_price_tree = {}
	tree_size = len(s_price_tree)-1

	
	for period in range(tree_size,-1,-1):
		optprice_period = []

		if(period == tree_size):
			for i in range(0,len(s_price_tree[period]),2):
				su = s_price_tree[period][i]
				sd = s_price_tree[period][i+1]
				cu = cd = 0
				early_up = (su-k_strike) if call else (k_strike-su)
				early_down = (sd-k_strike) if call else (k_strike-sd)
				
				cu = max(early_up,0)
				cd = max(early_down,0)

				optprice_period += [cu,cd]

		else:
			for i in range(0,len(opt_price_tree[period+1]),2):
				last_cu = opt_price_tree[period+1][i]
				last_cd = opt_price_tree[period+1][i+1]

				cp = 0

				if(american):
					sp = s_price_tree[period][i//2]
					early = (sp-k_strike) if call else (k_strike-sp)
					cp = max(early,0)


				calculated_cp = calculate_period_price(r_neutral_prob, last_cu, last_cd)
				cp = max(cp, calculated_cp)
				optprice_period += [cp]


		opt_price_tree[period] = optprice_period

	return opt_price_tree

def get_from_putcall_parity(opt_price, call):
	cash = k_strike*np.exp(-(rate-div)*h_period)
	if(call):
		return opt_price+cash-stock_price
	else:
		return opt_price+stock_price-cash

def get_probabilties(price_tree):
	probabilities = {}
	final_period = len(price_tree)-1
	price_list = price_tree[final_period]
	total = len(price_list)
	print(total)
	for i in range(total):
		price = '%.3f' %price_list[i]

		probabilities[price] = 1 if price not in probabilities else (probabilities[price]+1)

	return probabilities

def graph_probabilities(probabilities):

	od = collections.OrderedDict(sorted(probabilities.items()))
	keys = 	list(od.keys())
	vals = list(od.values())

	max_key = max(probabilities, key=probabilities.get)
	print(max_key) #55

	width = 1/1.5

	plt.title('Distributed chances')
	plt.bar(keys,vals, width, color='blue')
	plt.ylabel('Chance')
	plt.xlabel('Price')
	plt.show()






def setup():
	up, down = get_up_down()
	r_neutral_prob = get_risk_neutral_prob(up, down)
	s_price_tree = calculate_stock_prices(stock_price, up, down, n_period)
	# probabilities = get_probabilties(s_price_tree)
	# graph_probabilities(probabilities)

	opt_price_tree = calculate_option_from_tree(s_price_tree, r_neutral_prob, k_strike=k_strike, call=call, american=american)
	final_opt1_price = opt_price_tree[0][0]
	opt1_type = 'Call' if call else 'Put'
	print('Price of %s at K strike %f is: %f'%(opt1_type, k_strike, final_opt1_price))
	opt2_type = 'Call' if not call else 'Put'
	final_opt2_price = get_from_putcall_parity(final_opt1_price,call)
	print('Price of %s at K strike %f is: %f'%(opt2_type, k_strike, final_opt2_price))
	probabilities = get_probabilties(s_price_tree)
	graph_probabilities(probabilities)



setup()