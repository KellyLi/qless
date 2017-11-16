import time

from pprint import pprint
from FirebaseManager import FirebaseManager

class QueueManager:
	firebaseManager = FirebaseManager()

	# TODO: logic to add scheduled user
	def add_scheduled_user(self, name, doctor_name):
		print('add scheduled user')

	# check in logic starts here
	def check_in(self, name, is_walk_in):
		if is_walk_in:
			self.check_in_walk_in(name)
		else:
			self.check_in_scheduled(name)

	# logic for walk in check in
	def check_in_walk_in(self, name):
		predicted_wait_time = self.get_predicted_start_time()
		self.firebaseManager.add_walk_in_user(name, self.get_current_millis(), predicted_wait_time)

	# logic for scheduled check in
	def check_in_scheduled(self, name):
		queues = self.firebaseManager.get_queues()
		current_user = None
		doctor = None

		# traverse through doctor queues for users
		doctor_index = 0
		for queue in queues:
			if 'walk_in' not in queue:
				users = queue.values()[0]
				user_index = 0
				for user in users:
					if user.get('name') == name:
						current_user = user
						doctor = queue.keys()[0]
						break
					user_index = user_index + 1
				if current_user:
					break
			doctor_index = doctor_index + 1

		if current_user:
			# get predicted start time
			predicted_wait_time = self.get_predicted_start_time()
			self.firebaseManager.check_in_scheduled_user(doctor_index, doctor, user_index, self.get_current_millis(), predicted_wait_time)

	# TODO: helper function to get predicted start time from prediction model
	def get_predicted_start_time(self):
		return -1

	# helper function to get epoch current millis
	def get_current_millis(self):
		return int(round(time.time() * 1000))