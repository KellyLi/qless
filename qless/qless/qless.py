from flask import Flask, render_template, request
from FirebaseManager import FirebaseManager

app = Flask(__name__)
firebaseManager = FirebaseManager()

@app.route('/')
def index():
	return render_template('checkin.html')

@app.route('/checkin', methods=['POST'])
def check_in_submit():
	firstName = request.form['firstNameInput']
	lastName = request.form['lastNameInput']
	name = str(firstName + ' ' + lastName)
	return firebaseManager.addUser(1, 1, True, name, None)

@app.route('/checkin/success')
def check_in_success():
	return render_template('success.html')

@app.route('/data')
def get_data():
	return firebaseManager.getUsers()

if __name__ == "__main__":
	app.run()