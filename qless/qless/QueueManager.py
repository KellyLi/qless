import time

from pprint import pprint
from FirebaseManager import FirebaseManager

class QueueManager:
	def __init__(self):
		self.firebaseManager = FirebaseManager()
		self.users = {}

		self.cache_users()

		pprint(self.users)

	# get all users from db and store locally
	def cache_users(self):
		db_users = self.firebaseManager.get_users()
		for db_user in db_users:
			user_id = db_user.get('id')
			if user_id:
				self.users[user_id] = db_user

	# logic to add scheduled user
	def add_scheduled_user(self, user_id, name, doctor_name, scheduled_start_time):
		queue = self.firebaseManager.get_doctor_queue(doctor_name)

		data = {
			u'id': user_id,
			u'check_in_time': -1,
			u'is_checked_in': False,
			u'name': name,
			u'predicted_start_time': -1,
			u'scheduled_start_time': scheduled_start_time
		}

		if scheduled_start_time >= queue[-1]['scheduled_start_time']:
			queue.append(data)
		elif scheduled_start_time <= queue[0]['scheduled_start_time']:
			queue.insert(0, data)
		else:
			index = 0
			for user in queue:
				if scheduled_start_time < queue[index]['scheduled_start_time']:
					queue.insert(index, data)
					break
				index = index + 1

		self.firebaseManager.update_queue(doctor_name, queue)
		self.cache_users()

	# logic for walk in check in
	def add_walk_in(self, user_id, name):
		predicted_wait_time = self.get_predicted_start_time()
		queue = self.firebaseManager.get_walk_in_queue()
		for user in queue:
			if user.get('id') and user.get('id') == user_id:
				return False
		self.firebaseManager.add_walk_in_user(len(queue), user_id, name, self.get_current_millis(), predicted_wait_time)
		self.cache_users()
		return True

	# logic for scheduled check in
	def check_in_scheduled(self, user_id):
		queues = self.firebaseManager.get_queues()
		user = None
		doctor = None

		# traverse through doctor queues for users
		for current_doctor in queues:
			if 'walk_in' is not doctor:
				users = queues[current_doctor]
				user_index = 0
				for current_user in users:
					if current_user.get('id') == user_id:
						user = current_user
						doctor = current_doctor
						break
					user_index = user_index + 1
				if user:
					break

		if user:
			# get predicted start time
			predicted_wait_time = self.get_predicted_start_time()
			self.firebaseManager.check_in_scheduled_user(doctor, user_index, self.get_current_millis(), predicted_wait_time)

	# logic to page user (remove from doctor queue and add to paging queue)
	def page_user(self, user_id, room):
		queues = self.firebaseManager.get_queues()
		user = None
		doctor = None
		queue = None

		# traverse through doctor queues for users
		for current_doctor in queues:
			users = queues[current_doctor]
			index = 0
			for current_user in users:
				if current_user.get('id') == user_id:
					user = current_user
					doctor = current_doctor
					queue = users
					break
				index = index + 1

		if user:
			user[u'room'] = room
			user[u'doctor'] = doctor
			queue_size = len(self.firebaseManager.get_now_paging())

			# add user to now_paging
			self.firebaseManager.add_paging_user(queue_size, user)

			# remove user from current queue
			del queue[index]
			self.firebaseManager.update_queue(doctor, queue)

	# logic to seen user (remove from now paging queue and add to seen queue)
	def seen_user(self, user_id):
		users = self.firebaseManager.get_now_paging()
		user = None

		index = 0
		for current_user in users:
			if current_user.get('id') == user_id:
				user = current_user
				break
			index = index + 1

		if user:
			# add user to seen
			queue_size = len(self.firebaseManager.get_patients_seen())
			self.firebaseManager.add_seen_user(queue_size, user)

			# remove user from now_paging
			del users[index]
			self.firebaseManager.update_now_paging(users)

	# TODO: helper function to get predicted start time from prediction model
	def get_predicted_start_time(self):
		return -1

	# helper function to get epoch current millis
	def get_current_millis(self):
		return int(round(time.time() * 1000))