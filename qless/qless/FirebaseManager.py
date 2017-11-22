from firebase import firebase

class FirebaseManager:
	firebase = firebase.FirebaseApplication("https://qless-74979.firebaseio.com", None)

	def get_queues(self):
		return self.firebase.get('queues', '')

	def get_walk_in_queue(self):
		return self.firebase.get('queues/walk_in', '')

	def get_doctor_queue(self, doctor_name):
		path = "queues/" + doctor_name
		return self.firebase.get(path, '')

	def check_in_scheduled_user(self, doctor_name, user_index, current_time, predicted_start_time):
		path = "queues/" + doctor_name + "/" + str(user_index)
		self.firebase.put(path, "is_checked_in", True)
		self.firebase.put(path, "check_in_time", current_time)
		self.firebase.put(path, "predicted_start_time", predicted_start_time)

	def add_scheduled_user(self, doctor_name, data):
		path = "queues/"
		self.firebase.put(path, doctor_name, data)

	def add_walk_in_user(self, index, user_id, name, current_time, predicted_start_time):
		data = {
			index: {
				'id': user_id,
				'check_in_time': current_time,
				'name': name,
				'predicted_start_time': predicted_start_time,
			}
		}
		self.firebase.patch('queues/walk_in', data)

	def get_users(self):
		return self.firebase.get('users', '')