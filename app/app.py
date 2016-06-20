from flask import request, redirect, Flask, send_file, flash, render_template, url_for
# from flask_sqlalchemy import SQLAlchemy
from option_price_full import convert_parameters, calculate_opt_prices

app = Flask(__name__, static_url_path='')

# db = SQLAlchemy(app)

@app.route('/')
def index():
	print('I am back at index?')
	return send_file('index.html')

@app.route('/option_pricing_model', methods=['GET', 'POST'])
def option_pricing_model():
	if request.method == 'POST': #do calculation
		user_input = dict((key, request.form.getlist(key)[0]) for key in request.form.keys())
		curated_params = convert_parameters(user_input)

		print('it gets here before redirect')
		return redirect(url_for('option_pricing_view', **curated_params))
	
	print('do i get here?')
	return render_template('option_pricing_model.html')

@app.route('/option_pricing_view', methods=['GET'])
def option_pricing_view():
	print('----- HEEEREE --------')
	if request.method == "GET":
		print('args %s' % request.args)
		option_parameters = dict((key, request.args.getlist(key)[0]) for key in request.args.keys())
		print('option parementers --> %s' % option_parameters)
		calculated_parameters = calculate_opt_prices(option_parameters)
		print(' calculated params: %s' %calculated_parameters)

		joined_parameters = dict(option_parameters)
		joined_parameters.update(calculated_parameters)

		# joined_parameters = {**option_parameters, **calculated_parameters}
		# joined_parameters = 

		print(joined_parameters)

		return render_template('option_pricing_view.html' ,**joined_parameters)
		

if __name__ == '__main__':
	app.run(host='127.0.0.1')
