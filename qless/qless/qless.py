from flask import Flask, render_template, request
from QueueManager import QueueManager

app = Flask(__name__)
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
	return '{}'

@app.route('/checkin/success')
def check_in_success():
	return render_template('success.html')

@app.route('/test')
def test():
	#queueManager.add_scheduled_user(20, "bruh", "doctor_hudson", 1510513232)
	#queueManager.add_walk_in(21, "bruvvv")
	#queueManager.check_in_scheduled(20)
	#queueManager.page_user(20, "roooom")
	#queueManager.seen_user(20)
	return '{}'

if __name__ == "__main__":
	app.run()