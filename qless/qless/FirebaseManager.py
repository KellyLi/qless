from firebase import firebase
from flask import jsonify

class FirebaseManager:
	firebase = firebase.FirebaseApplication("https://qless-74979.firebaseio.com", None)

	def getUsers(self):
		data = self.firebase.get('', '')
		return jsonify(data)

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