#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import collections
import scipy.stats as st

call = True

stock_price = 315
k_strike = 300
rate = 0.04
div=0
vol = 0.9
t_time = 1/52


def get_d1_d2():
	period_vol = vol * np.sqrt(t_time)
	d1 = (np.log(stock_price/k_strike) + (rate-div+ ((vol**2)/2))*t_time)/period_vol
	d2 = d1 - period_vol
	return d1,d2

def get_normal_cdf(distributions, call):
	if not call:
		distributions = [ -d for d in distributions]
	return [st.norm.cdf(d) for d in distributions]

def calculate_option_price(probs, call):
	first_half = stock_price * np.exp(-div*t_time)*probs[0]
	second_half = k_strike * np.exp(-rate*t_time)*probs[1]
	opt_price = first_half - second_half if call else second_half - first_half
	return opt_price

def setup():
	distributions = get_d1_d2()
	print(distributions)
	probs = get_normal_cdf(distributions,call)
	print(probs)
	opt_price = calculate_option_price(probs, call)
	print(opt_price)

setup()