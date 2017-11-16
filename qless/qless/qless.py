from flask import Flask, render_template, request
from FirebaseManager import FirebaseManager
from QueueManager import QueueManager

app = Flask(__name__)
firebaseManager = FirebaseManager()
queueManager = QueueManager()

@app.route('/')
def index():
	return render_template('checkin.html')

@app.route('/checkin', methods=['POST'])
def check_in_submit():
	firstName = request.form['firstNameInput']
	lastName = request.form['lastNameInput']
	name = str(firstName + ' ' + lastName)
	isWalkin = True if 'isWalkin' in request.form else False
	return firebaseManager.addUser(1, 1, isWalkin, name, None)

@app.route('/checkin/success')
def check_in_success():
	return render_template('success.html')

@app.route('/test')
def test():
	queueManager.check_in("A. Balone", False)
	return '{}'

if __name__ == "__main__":
	app.run()