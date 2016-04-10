import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import collections
from black_scholes_model import Black_Scholes
from binomial_option_pricing import Binomial_Model

class Option:

	american = True
	call = True
	ticker = 'GS'
	stock_price = 150.47
	k_strike = 170
	t_time = 1
	n_period = 20
	rate = 0.03
	div = 3
	vol = 0.25
	h_period = 0

	black_scholes_opt = 0
	black_scholes_price = 0
	binomial_model_opt = 0
	binomial_model_price = 0


	def __init__(self, american, call, ticker,
				stock_price, k_strike, t_time, vol, rate, n_period, div):
		self.american = american
		self.call = call
		self.ticker = ticker
		self.stock_price = stock_price
		self.k_strike = k_strike
		self.t_time = t_time
		self.vol = vol
		self.rate = rate
		self.div = div
		self.n_period = n_period
		self.h_period = (t_time/n_period)
		self.black_scholes_price = 0
		self.binomial_model_price = 0
		self.black_scholes_opt = Black_Scholes(call=self.call, stock_price=self.stock_price, 
	 									k_strike=self.k_strike, t_time=self.t_time,
	 									vol=self.vol, rate=self.rate, div=self.div)
		self.binomial_model_opt = Binomial_Model(american=self.american, call=self.call, stock_price=self.stock_price, k_strike=self.k_strike, 
											t_time=self.t_time, vol=self.vol, rate=self.rate, n_period=self.n_period, div=self.div)


	def get_black_scholes_price(self):
		self.black_scholes_price = self.black_scholes_opt.get_option_price()
		return self.black_scholes_price

	def get_binomial_model_price(self):
		self.binomial_model_price = self.binomial_model_opt.get_option_price()
		return self.binomial_model_price

	def get_black_scholes_class(self):
		return self.black_scholes_opt

	def get_binomial_model_class(self):
		return self.binomial_model_opt


	def get_new_black_scholes_class(self, call, stock_price, k_strike, t_time, vol, rate, div):
		self.black_scholes_opt = Black_Scholes(call=call, stock_price=stock_price, k_strike=k_strike, 
											t_time=t_time, vol=vol, rate=rate, div=div)
		return self.black_scholes_opt

	def get_new_binomial_model_class(self, american, call, stock_price, k_strike, t_time, vol, rate, n_period, div):
		self.binomial_model_opt = Binomial_Model(american=american, call=call, stock_price=stock_price, k_strike=k_strike, 
												t_time=t_time, vol=vol, rate=rate, n_period=n_period, div=div)

		return self.binomial_model_opt

	def get_from_put_call_parity(self):
		cash = self.k_strike*np.exp(-(self.rate-self.div)*self.h_period)
		other_prices = {'black_scholes_price':self.black_scholes_price, 'binomial_model_price':self.binomial_model_price}
		get_function = lambda opt_price: (opt_price+cash-self.stock_price) if self.call else (opt_price+self.stock_price-cash)
		other_prices = {opt_type: get_function(opt_price) for opt_type, opt_price in other_prices.items()}
		return other_prices


	def graph_sprobabilities_bm(self):
		probabilities = self.binomial_model_opt.probabilities
		od = collections.OrderedDict(sorted(probabilities.items()))
		
		keys = 	list(od.keys())
		vals = list(od.values())

		width = 1/1.5
		title = 'Normal Distribution of outcomes for %s with vol = %.4f' % (self.ticker, self.vol)
		plt.title(title)
		plt.bar(keys,vals, width, color='blue')
		plt.ylabel('Chances of this being the final outcome')
		plt.xlabel('Price')
		plt.show()

	def get_prob_from_zscore(self):
		rand_vars = self.binomial_model_opt.get_mean_stdev_from_probs()
		mean = rand_vars['mean']
		stdev = rand_vars['stdev']
		z_score = (self.k_strike-mean)/stdev
		cdf = st.norm.cdf(z_score)
		prob = min(cdf, 1-cdf)
		return prob





