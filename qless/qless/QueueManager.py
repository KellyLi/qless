import time

from pprint import pprint
from FirebaseManager import FirebaseManager

class QueueManager:
	def __init__(self):
		self.firebaseManager = FirebaseManager()
		self.doctor_indexes = {}
		self.users = {}

		self.cache_doctors()
		self.cache_users()

		pprint(self.users)
		pprint(self.doctor_indexes)

	# get all users from db and store locally
	def cache_users(self):
		db_users = self.firebaseManager.get_users()
		for db_user in db_users:
			user_id = db_user.get('id')
			if user_id:
				self.users[user_id] = db_user

	# get all doctors from db and store locally
	def cache_doctors(self):
		queues = self.firebaseManager.get_queues()
		doctor_index = 0
		for queue in queues:
			self.doctor_indexes[queue.keys()[0]] = doctor_index
			doctor_index = doctor_index + 1

	# TODO: logic to add scheduled user
	def add_scheduled_user(self, user_id, name, doctor_name, scheduled_start_time):
		print('add scheduled user')

	# logic for walk in check in
	def check_in_walk_in(self, user_id, name):
		predicted_wait_time = self.get_predicted_start_time()
		queue = self.firebaseManager.get_walk_in_queue()
		for user in queue.values():
			if user.get('id') and user.get('id') == user_id:
				return False
		self.firebaseManager.add_walk_in_user(user_id, name, self.get_current_millis(), predicted_wait_time)
		self.cache_users()
		return True

	# logic for scheduled check in
	def check_in_scheduled(self, user_id):
		queues = self.firebaseManager.get_queues()
		current_user = None
		doctor = None

		# traverse through doctor queues for users
		for queue in queues:
			if 'walk_in' not in queue:
				users = queue.values()[0]
				user_index = 0
				for user in users:
					if user.get('id') == user_id:
						current_user = user
						doctor = queue.keys()[0]
						break
					user_index = user_index + 1
				if current_user:
					break

		if current_user:
			# get predicted start time
			predicted_wait_time = self.get_predicted_start_time()
			self.firebaseManager.check_in_scheduled_user(self.doctor_indexes[doctor], doctor, user_index, self.get_current_millis(), predicted_wait_time)

	# TODO: helper function to get predicted start time from prediction model
	def get_predicted_start_time(self):
		return -1

	# helper function to get epoch current millis
	def get_current_millis(self):
		return int(round(time.time() * 1000))