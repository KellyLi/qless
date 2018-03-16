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

	def get_now_paging(self):
		return self.firebase.get("now_paging", '')

	def get_patients_seen(self):
		return self.firebase.get("patients_seen", '')

	def check_in_scheduled_user(self, doctor_name, user_index, current_time, predicted_start_time):
		path = "queues/" + doctor_name + "/" + str(user_index)
		self.firebase.put(path, "is_checked_in", True)
		self.firebase.put(path, "check_in_time", current_time)
		self.firebase.put(path, "predicted_start_time", predicted_start_time)

	def update_queue(self, doctor_name, data):
		path = "queues/"
		self.firebase.put(path, doctor_name, data)

	def update_now_paging(self, data):
		self.firebase.put('', "now_paging", data)

	def update_seen_users(self, data):
		self.firebase.put('', "patients_seen", data)

	def update_users(self, data):
		self.firebase.put('', "users", data)

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

	def add_paging_user(self, index, data):
		self.firebase.patch("now_paging", {index: data})

	def add_seen_user(self, index, data):
		self.firebase.patch("patients_seen", {index: data})

	def get_users(self):
		return self.firebase.get('users', '')

	def add_user(self, user_id, name):
		users = self.get_users()

		if users is None:
			users = []

		# first check if user is existing
		index = 0
		for user in users:
			if user.get('id') == user_id:
				path = "users/" + str(index)
				self.firebase.put(path, "id", user_id)
				self.firebase.put(path, "name", name)
				return
			index = index + 1

		# otherwise append new user
		new_user = {
			len(users): {
				"id": user_id,
				"name": name
			}
		}
		self.firebase.patch("users", new_user)
