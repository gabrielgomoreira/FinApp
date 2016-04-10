#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import collections
import scipy.stats as st
from vol_app import calculate_vol


class Black_Scholes:

	def __init__(self, call, stock_price, k_strike, t_time, vol, rate, div):
		self.call = call
		self.stock_price = stock_price
		self.k_strike = k_strike
		self.t_time = t_time
		self.vol = vol
		self.rate = rate
		self.div = div

		self.setup()

		
	def get_d1_d2(self):
		period_vol = vol * np.sqrt(t_time)
		d1 = (np.log(stock_price/k_strike) + (rate-div+ ((vol**2)/2))*t_time)/period_vol
		d2 = d1 - period_vol
		return d1,d2

	def get_normal_cdf(self, distributions, call):
		if not call:
			distributions = [ -d for d in distributions]
		return [st.norm.cdf(d) for d in distributions]

	def calculate_option_price(self, probs, call):
		first_half = stock_price * np.exp(-div*t_time)*probs[0]
		second_half = k_strike * np.exp(-rate*t_time)*probs[1]
		opt_price = first_half - second_half if call else second_half - first_half
		return opt_price

	def setup(self):
		distributions = self.get_d1_d2()
		probs = self.get_normal_cdf(distributions,call)
		opt_price = calculate_option_price(probs, call)
		return opt_price
