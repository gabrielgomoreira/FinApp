#!/usr/bin/env python3
import numpy as np
import scipy.stats as st

class Black_Scholes:

	call = True
	stock_price = 150
	k_strike = 170
	t_time = 1
	vol = 0.25
	rate = 0.01
	div = 0

	def __init__(self, call, stock_price, k_strike, t_time, vol, rate, div):
		self.call = call
		self.stock_price = stock_price
		self.k_strike = k_strike
		self.t_time = t_time
		self.vol = vol
		self.rate = rate
		self.div = div

	def get_d1_d2(self):
		period_vol = self.vol * np.sqrt(self.t_time)
		d1 = (np.log(self.stock_price/self.k_strike) + (self.rate-self.div+ ((self.vol**2)/2))*self.t_time)/period_vol
		d2 = d1 - period_vol
		return d1,d2

	def get_normal_cdf(self, distributions, call):
		if not call:
			distributions = [ -d for d in distributions]
		return [st.norm.cdf(d) for d in distributions]

	def calculate_option_price(self, probs, call):
		first_half = self.stock_price * np.exp(-self.div*self.t_time)*probs[0]
		second_half = self.k_strike * np.exp(-self.rate*self.t_time)*probs[1]
		opt_price = first_half - second_half if call else second_half - first_half
		return opt_price

	def get_option_price(self):
		distributions = self.get_d1_d2()
		probs = self.get_normal_cdf(distributions,self.call)
		opt_price = self.calculate_option_price(probs, self.call)
		return opt_price
