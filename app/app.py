from flask import request, redirect, Flask, send_file, flash, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from option_price_full import convert_parameters

app = Flask(__name__, static_url_path='')

db = SQLAlchemy(app)

@app.route('/')
def index():
	print('I am back at index?')
	return send_file('index.html')

@app.route('/option_pricing_model', methods=['GET', 'POST'])
def option_pricing_model():
	if request.method == 'POST': #do calculation
		# print(request.form)
		# american = request.form['american']
		# call = request.form['call']
		# ticker = request.form['ticker']
		# t_time = request.form['t_time']
		# k_strike = request.form['k_strike']
		user_input = dict((key, request.form.getlist(key)[0]) for key in request.form.keys())
		curated_params = convert_parameters(user_input)
		print(curated_params)

		print('it gets here before redirect')
		return redirect(url_for('option_pricing_view', american=american, call=call,
				ticker=ticker, t_time=t_time, k_strike=k_strike))
	
	print('do i get here?')
	return render_template('option_pricing_model.html')

@app.route('/option_pricing_view/', methods=['GET'])
def option_pricing_view():
	print('----- HEEEREE --------')
	if request.method == "GET":
		american = request.args['american']
		call = request.args['call']
		ticker = request.args['ticker']
		t_time = request.args['t_time']
		k_strike = request.args['k_strike']
		return render_template('option_pricing_view.html')
	# if request.method == 'POST':
	# 	american = request.form['american']
	# 	call = request.form['call']
	# 	ticker = request.form['ticker']
	# 	t_time = request.form['t_time']
	# 	k_strike = request.form['k_strike']
		# return redirect(url_for('option_pricing_view'))
		# return redirect(url_for('option_pricing_research'))

if __name__ == '__main__':
	app.run(host='127.0.0.1')
