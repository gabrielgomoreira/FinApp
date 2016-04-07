#!/usr/bin/env python3

import numpy as np

rate = 0.04
div=0
n_period = 2
h_period= (1/12)
vol = 0.9
stock_price = 3.16
call = True
k_strike = 100
american = False


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
	s_price_tree = {0:stock_price}
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
				if(call):
					cu = max(su-k_strike,0)
					cd = max(sd-k_strike,0)
				else:
					cu = max(k_strike-su,0)
					cd = max(k_strike-sd,0)

				optprice_period += [cu,cd]
		else:
			for i in range(0,len(optprice_period[period+1]),2):
				last_cu = optprice_period[period+1][i]
				last_cd = optprice_period[period+1][i+1]

				cp = 0

				if(american):
					sp = s_price_tree[period][i]
					if(call):
						cp = max(su-k_strike,0)
					else:
						cp = max(k_strike-su,0)

				calculated_cp = calculate_period_price(r_neutral_prob, last_cu, last_cd)
				cp = max(cp, calculated_cp)
				optprice_period += [cp]


		opt_price_tree[period] = optprice_period

	return opt_price_tree



def setup():
	up, down = get_up_down()
	r_neutral_prob = get_risk_neutral_prob(up, down)
	s_price_tree = calculate_stock_prices(stock_price, up, down, n_period)
	opt_price_tree = calculate_option_from_tree(s_price_tree, r_neutral_prob, k_strike=k_strike, call=call, american=american)
	print(opt_price_tree)

setup()