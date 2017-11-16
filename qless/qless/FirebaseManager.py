from firebase import firebase
from flask import jsonify

class FirebaseManager:
	firebase = firebase.FirebaseApplication("https://qless-74979.firebaseio.com", None)

	def addUser(self, appointment_end, appointment_start, is_walk_in, name, appointment_time):
		data = {
			'appointment_end': appointment_end,
			'appointment_start': appointment_start,
			'is_walk_in': is_walk_in,
			'name': name
		}

		if is_walk_in and appointment_time:
			data['appointment_time'] = appointment_time
		
		self.firebase.post('', data)

		return jsonify(data)

	def getQueues(self):
		return self.firebase.get('queues', '')

	def checkInScheduledUser(self, doctor_index, doctor_name, user_index, current_time, predicted_start_time):
		path = "queues/" + str(doctor_index) + "/" + doctor_name + "/" + str(user_index)
		self.firebase.put(path, "is_checked_in", True)
		self.firebase.put(path, "check_in_time", current_time)
		self.firebase.put(path, "predicted_start_time", predicted_start_time)

	def addWalkInUser(self, name, current_time, predicted_start_time):
		data = {
			'check_in_time': current_time,
			'name': name,
			'predicted_start_time': predicted_start_time,
		}
		self.firebase.post('queues/0/walk_in', data)