#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import collections

class Binomial_Model:

	american = True
	call = True
	stock_price = 41
	k_strike = 40
	rate = 0.08
	div = 3
	t_time = 1
	n_period = 3
	h_period= 4
	vol = 0.3
	probabilities = 0

	def __init__(self, american, call,
				stock_price, k_strike, t_time, vol, rate, n_period, div):
		self.american = american
		self.call = call
		self.stock_price = stock_price
		self.k_strike = k_strike
		self.t_time = t_time
		self.vol = vol
		self.rate = rate
		self.n_period = n_period
		self.div = div
		self.h_period = (t_time/n_period)
		self.probabilities = 0


	def get_up_down(self):
		up = np.exp( ((self.rate-self.div)*(self.h_period))   + (self.vol*np.sqrt(self.h_period)  ))
		down = np.exp( ((self.rate-self.div)*self.h_period) - (self.vol*np.sqrt(self.h_period))  )
		return up, down

	def get_risk_neutral_prob(self, up=0, down=0):
		return ((np.exp((self.rate-self.div)*self.h_period)-down)/(up-down))

	def calculate_period_price(self, r_neutral_prob=0.5, opt_up=0, opt_down=0):
		price = ((opt_up*r_neutral_prob)+(opt_down*(1-r_neutral_prob)))
		pv = np.exp(-self.rate*self.h_period)
		return pv * price

	def calculate_stock_prices(self, stock_price, up, down, n_period):
		s_price_tree = {0:[stock_price]}
		for period in range(1, self.n_period+1):
			sprices_for_period = []
			if(period == 1): # first istance
				sprices_for_period = [self.stock_price*up, self.stock_price*down]
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

	def calculate_option_from_tree(self, s_price_tree, r_neutral_prob, k_strike, call=True, american=True):
		opt_price_tree = {}
		tree_size = len(s_price_tree)-1

		
		for period in range(tree_size,-1,-1):
			optprice_period = []

			if(period == tree_size):
				for i in range(0,len(s_price_tree[period]),2):
					su = s_price_tree[period][i]
					sd = s_price_tree[period][i+1]
					cu = cd = 0
					early_up = (su-self.k_strike) if call else (self.k_strike-su)
					early_down = (sd-self.k_strike) if call else (self.k_strike-sd)
					
					cu = max(early_up,0)
					cd = max(early_down,0)

					optprice_period += [cu,cd]

			else:
				for i in range(0,len(opt_price_tree[period+1]),2):
					last_cu = opt_price_tree[period+1][i]
					last_cd = opt_price_tree[period+1][i+1]

					cp = 0

					if(self.american):
						sp = s_price_tree[period][i//2]
						early = (sp-self.k_strike) if call else (self.k_strike-sp)
						cp = max(early,0)


					calculated_cp = self.calculate_period_price(r_neutral_prob, last_cu, last_cd)
					cp = max(cp, calculated_cp)
					optprice_period += [cp]


			opt_price_tree[period] = optprice_period

		return opt_price_tree

	def get_from_putcall_parity(self, opt_price, call):
		cash = self.k_strike*np.exp(-(self.rate-self.div)*self.h_period)
		if(call):
			return opt_price+cash-self.stock_price
		else:
			return opt_price+self.stock_price-cash

	def get_probabilties(self, price_tree):
		probabilities = {}
		final_period = len(price_tree)-1
		price_list = price_tree[final_period]
		total = len(price_list)
		for i in range(total):
			price = '%.3f' %price_list[i]

			probabilities[price] = 1 if price not in probabilities else (probabilities[price]+1)

		self.probabilities = probabilities
		return self.probabilities

	def get_mean_stdev_from_probs(self):
		mean = 0
		count = 0
		for price in self.probabilities:
			count_int = int(self.probabilities[price])
			self.probabilities[price] = count_int
			mean += float(price) * count_int
			count += count_int
		mean /= count
		var = 0
		for price in self.probabilities:
			var += ((float(price) - mean)**2) * self.probabilities[price]
		var /= (count-1)
		stdev = np.sqrt(var)
		return {'mean':mean, 'stdev':stdev, 'var':var}

	def get_option_price(self):
		up, down = self.get_up_down()
		r_neutral_prob = self.get_risk_neutral_prob(up, down)
		s_price_tree = self.calculate_stock_prices(self.stock_price, up, down, self.n_period)
		opt_price_tree = self.calculate_option_from_tree(s_price_tree, r_neutral_prob, k_strike=self.k_strike, call=self.call, american=self.american)
		final_opt1_price = opt_price_tree[0][0]
		self.get_probabilties(s_price_tree)
		return final_opt1_price