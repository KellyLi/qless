from firebase import firebase

class FirebaseManager:
	firebase = firebase.FirebaseApplication("https://qless-74979.firebaseio.com", None)

	def get_queues(self):
		return self.firebase.get('queues', '')

	def check_in_scheduled_user(self, doctor_index, doctor_name, user_index, current_time, predicted_start_time):
		path = "queues/" + str(doctor_index) + "/" + doctor_name + "/" + str(user_index)
		self.firebase.put(path, "is_checked_in", True)
		self.firebase.put(path, "check_in_time", current_time)
		self.firebase.put(path, "predicted_start_time", predicted_start_time)

	def add_scheduled_user(self, name, doctor_index, doctor_name, scheduled_start_time):
		path = "queues/" + str(doctor_index) + "/" + doctor_name
		data = {
			'check_in_time': -1,
			'is_checked_in': False,
			'name': name,
			'predicted_start_time': -1,
			'scheduled_start_time': scheduled_start_time
		}
		self.firebase.post(path, data)

	def add_walk_in_user(self, name, current_time, predicted_start_time):
		data = {
			'check_in_time': current_time,
			'name': name,
			'predicted_start_time': predicted_start_time,
		}
		self.firebase.post('queues/0/walk_in', data)