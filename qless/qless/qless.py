from flask import Flask, render_template, request, jsonify
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
	#queueManager.add_walk_in(21, "bruvsssvv")
	#queueManager.add_scheduled_user(20, "bruh", "doctor_hudson", 1510513232)
	#queueManager.check_in_scheduled(20)
	#queueManager.check_in_scheduled(4)
	#queueManager.page_user(20, "roooom")
	#queueManager.seen_user(20)
	return '{}'

# user_id(int), name(str), doctor_name(str), scheduled_start_time(int)
@app.route('/schedule/add', methods=['POST'])
def schedule_add():
	user_id = None
	name = None
	doctor_name = None
	scheduled_start_time = None

	if request.form:
		user_id = int(request.form.get('user_id'))
		name = request.form.get('name')
		doctor_name = request.form.get('doctor_name')
		scheduled_start_time = int(request.form.get('scheduled_start_time'))

	if user_id and name and doctor_name and scheduled_start_time:
		queueManager.add_scheduled_user(user_id, name, doctor_name, scheduled_start_time)

	response = {
		"user_id": user_id,
		"name": name,
		"doctor_name": doctor_name,
		"scheduled_start_time": scheduled_start_time
	}

	return jsonify(response)

# user_id(int)
@app.route('/schedule/checkin', methods=['POST'])
def schedule_check_in():
	user_id = None

	if request.form:
		user_id = int(request.form.get('user_id'))

	if user_id:
		queueManager.check_in_scheduled(user_id)

	response = {
		"user_id": user_id
	}

	return jsonify(response)

# user_id(int), name(str)
@app.route('/walkin', methods=['POST'])
def walk_in():
	user_id = None
	name = None

	if request.form:
		user_id = int(request.form.get('user_id'))
		name = request.form.get('name')

	if user_id and name:
		queueManager.add_walk_in(user_id, name)

	response = {
		"user_id": user_id,
		"name": name
	}

	return jsonify(response)

# user_id(int), room(str)
@app.route('/page', methods=['POST'])
def page():
	user_id = None
	room = None

	if request.form:
		user_id = int(request.form.get('user_id'))
		room = request.form.get('room')

	if user_id and room:
		queueManager.page_user(user_id, room)

	response = {
		"user_id": user_id,
		"room": room
	}

	return jsonify(response)

# user_id(int)
@app.route('/seen', methods=['POST'])
def seen():
	user_id = None

	if request.form:
		user_id = int(request.form.get('user_id'))

	if user_id:
		queueManager.seen_user(user_id)

	response = {
		"user_id": user_id
	}

	return jsonify(response)

if __name__ == "__main__":
	app.run()