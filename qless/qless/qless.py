from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('checkin.html')

@app.route('/checkin', methods=['POST'])
def check_in_submit():
	_firstName = request.form['firstNameInput']
	_lastName = request.form['lastNameInput']
	return jsonify({
			'first_name': _firstName,
			'last_name': _lastName
		})

@app.route('/checkin/success')
def check_in_success():
	return render_template('success.html')

@app.route('/data')
def get_data():
	return jsonify({
		'patient': "patient_string",
		'appointment_time': 'DateTime',
		'is_walk_in': True,
		'appointment_length': 'DateTime'
	})


if __name__ == "__main__":
	app.run()