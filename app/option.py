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
		self.american = (american == 'True')
		self.call = (call == 'True')
		self.ticker = ticker
		self.stock_price = float(stock_price)
		self.k_strike = float(k_strike)
		self.t_time = float(t_time)
		self.vol = float(vol)
		self.rate = float(rate)
		self.div = float(div)
		self.n_period = int(n_period)
		self.h_period = (float(t_time)/int(n_period))
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


	def get_prob_from_zscore(self):
		rand_vars = self.binomial_model_opt.get_mean_stdev_from_probs()
		mean = rand_vars['mean']
		stdev = rand_vars['stdev']
		z_score = (self.k_strike-mean)/stdev
		cdf = st.norm.cdf(z_score)
		prob = min(cdf, 1-cdf)
		rand_vars['prob'] = prob
		return rand_vars

	def graph_sprobabilities_bm(self):
		rand_vars = self.get_prob_from_zscore()
		probabilities = self.binomial_model_opt.probabilities
		od = collections.OrderedDict(sorted(probabilities.items()))
		
		keys = 	list(od.keys())
		vals = list(od.values())

		width = 1
		title = '%s\'s distribtuion w/ vol %.4f. Mean: %.2f, STEDV: %.2f, PROB: %.4f' % (self.ticker, self.vol, rand_vars['mean'], rand_vars['stdev'], rand_vars['prob'])
		plt.title(title)
		plt.bar(keys,vals, width, color='blue')
		plt.ylabel('Chances of this being the final outcome')
		plt.xlabel('Price')
		plt.show()

	def graph_binomial_convergence(self, binomial_dict):
		"""
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
		Black Scholes Pirce 39.581683 
		{1: 50.09687943007085, 2: 36.542582435749878, 3: 43.063509629441164, 4: 38.37619403881363, 5: 41.6097982184776, 6: 38.965803280411421, 7: 40.989017717552905, 8: 39.239476986143458, 9: 40.645594832026291, 10: 39.390892424824294, 11: 40.427776498752642, 12: 39.483763603290079, 13: 40.277361562835239, 14: 39.544690156886908, 15: 40.167275007556938, 16: 39.586571101890705, 17: 40.083223358182472, 18: 39.616344758887799, 19: 40.016951388841427, 20: 39.638038990961434, 21: 39.963359189711561, 22: 39.654133094308378, 23: 39.919126544988281, 24: 39.6662256646202, 25: 39.881999098174994}
		Put-Call Parity: {'binomial_model_price': 68.917431170224233, 'black_scholes_price': 68.617115454168868}
		Rand Vars and Prob: {'mean': 297.58461444354054, 'prob': 0.44808648636919335, 'stdev': 134.75076860002014, 'var': 18157.76963829617}

		
		# bs_price = 39.581683
		# binomial_dict = {1: 50.09687943007085, 2: 36.542582435749878, 3: 43.063509629441164, 4: 38.37619403881363, 5: 41.6097982184776, 6: 38.965803280411421, 7: 40.989017717552905, 8: 39.239476986143458, 9: 40.645594832026291, 10: 39.390892424824294, 11: 40.427776498752642, 12: 39.483763603290079, 13: 40.277361562835239, 14: 39.544690156886908, 15: 40.167275007556938, 16: 39.586571101890705, 17: 40.083223358182472, 18: 39.616344758887799, 19: 40.016951388841427, 20: 39.638038990961434, 21: 39.963359189711561, 22: 39.654133094308378, 23: 39.919126544988281, 24: 39.6662256646202, 25: 39.881999098174994}

		"""
		bs_price = binomial_model_price
		binomial_dict = {}
		for n in range(1,26):
			print(n)
			self.get_new_binomial_model_class(self.american, self.call, self.stock_price, self.k_strike, self.t_time, self.vol, self.rate, n, self.div)
			binomial_price = self.get_binomial_model_price()
			binomial_dict[n] = binomial_price

		print(binomial_dict)
		title = 'Binomial Model Convergence to Black Scholes Price of %.3f for %s with vol %.3f and prob %.4f' % (bs_price, self.ticker, self.vol, rand_vars['prob'])

		od = collections.OrderedDict(sorted(binomial_dict.items()))
		
		keys = 	list(od.keys())
		vals = list(od.values())
		average = np.mean(vals)
		average_list2plot = []
		bs_price_list2plot = []
		for i in vals:
			average_list2plot += [average]
			bs_price_list2plot += [bs_price]

		width = 1
		title = 'Binomial Model Convergence to Black Scholes Price of %.3f for %s with vol %.3f and prob %.4f' % (bs_price, 'TSLA', 0.433764, 0.44808648636919335)

		plt.title(title)
		plt.plot(keys,vals, label='Price per (n)', linewidth=2.0, color='r')
		plt.plot(keys,average_list2plot, color='b', label='Avg of BM prices', linestyle='dotted')
		plt.plot(keys,bs_price_list2plot, color='g', label='Black Scholes Price', linestyle='--')
		plt.legend(loc='upper right')
		plt.ylabel('Binomial Model Price')
		plt.xlabel('Number of (n) binomial periods')
		plt.grid(True)
		plt.show()








