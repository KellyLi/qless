import requests

def post_request(path, data):
	host = "http://localhost:5000"
	url = host + path
	print(url)

	r = requests.post(url, data)
	print(r)

def schedule_add():
	path = "/schedule/add"

	data = {
		"user_id": 20,
		"name": "bruh bromie",
		"doctor_name": "doctor_hudson",
		"scheduled_start_time": 1510513232
	}

	post_request(path, data)

def schedule_check_in():
	path = "/schedule/checkin"

	data = {
		'user_id': 4
	}

	post_request(path, data)

def walk_in():
	path = "/walkin"

	data = {
		"user_id": 21,
		"name": "huh homie"
	}

	post_request(path, data)

def page():
	path = "/page"

	data = {
		"user_id": 21,
		"room": "room ABCDEF"
	}

	post_request(path, data)

def seen():
	path = "/seen"

	data = {
		"user_id": 21
	}

	post_request(path, data)

#schedule_check_in()
#schedule_add()
#walk_in()
#page()
#seen()