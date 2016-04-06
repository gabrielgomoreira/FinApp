#!/usr/bin/env python3

import numpy as np

rate = 0
div=0
n_periods = 1
t_time = 1
h_period=1
vol = 0
call = True

def get_risk_neutral_prob(up=0, down=0):
	return ((np.exp((rate-div)*h_period)-down)/(up-down))

def get_up_down():
	up = np.exp(((rate-div)*h_period))+(vol*(h_period**0.5))
	down = up = np.exp(((rate-div)*h_period))-(vol*(h_period**0.5))
	return up, down

def calculate_period_price(r_neutral_prob=0.5, opt_up=0, opt_down=0):
	price = ((opt_up*r_neutral_prob)+(opt_down*(1-r_neutral_prob)))
	pv = np.exp(-rate*h_period)
	return pv * price

def calculate_stock_prices(s, up, down, h_period):
	s_price_tree = {}
	for period in range(h_period):
		if(not period): # first istance
			s_price_tree[period] = [s*up, s*down]
		else:
			prices_for_period = []
			for i in range(0,len(s_price_tree[h-1],2):
				




def setup():
	up, down = get_up_down()
	r_neutral_prob = get_up_down(up, down)


