import time

from pprint import pprint
from FirebaseManager import FirebaseManager
from rmodel import estimateWaitTime

class QueueManager:
	def __init__(self):
		self.firebaseManager = FirebaseManager()
		self.users = {}

		self.cache_users()

	# get all users from db and store locally
	def cache_users(self):
		db_users = self.firebaseManager.get_users()
		for db_user in db_users:
			user_id = db_user.get('id')
			if user_id:
				self.users[user_id] = db_user
		#pprint(self.users)

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
		self.firebaseManager.add_user(user_id, name)
		self.cache_users()

	# logic for walk in check in
	def add_walk_in(self, user_id, name):
		current_time = self.get_current_millis()
		predicted_wait_time = self.get_predicted_start_time(current_time, True, 'walk_in', None)
		queue = self.firebaseManager.get_walk_in_queue()
		for user in queue:
			if user.get('id') and user.get('id') == user_id:
				return False
		self.firebaseManager.add_walk_in_user(len(queue), user_id, name, current_time, predicted_wait_time)
		self.firebaseManager.add_user(user_id, name)
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
			current_time = self.get_current_millis()
			predicted_wait_time = self.get_predicted_start_time(current_time, False, doctor, user.get('scheduled_start_time'))
			self.firebaseManager.check_in_scheduled_user(doctor, user_index, current_time, predicted_wait_time)

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
				break

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
			user['seen_time'] = self.get_current_millis()
			self.firebaseManager.add_seen_user(queue_size, user)

			# remove user from now_paging
			del users[index]
			self.firebaseManager.update_now_paging(users)

	# TODO: helper function to get predicted start time from prediction model
	def get_predicted_start_time(self, current_time, is_walk_in, doctor_name, appointment_time):
		# 2. weekday, # string ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
		weekday = time.strftime("%A", time.localtime(current_time/1000))
		weekday = weekday.lower()[:3]

		# 3. queue_length, # number
		if is_walk_in:
			queue = self.firebaseManager.get_walk_in_queue()
		else:
			queue = self.firebaseManager.get_doctor_queue(doctor_name)

		# calculations done in seconds
		date = time.strftime("%m/%d/%Y", time.localtime(current_time/1000))
		epoch_start_date = int(time.mktime(time.strptime(date, "%m/%d/%Y")))
		epoch_end_date = epoch_start_date + (86400 - 1)

		queue_length = 0;
		for user in queue:
			if is_walk_in:
				queue_time = user.get('check_in_time')/1000
			else:
				queue_time = user.get('scheduled_start_time')/1000

			if queue_time >= epoch_start_date and queue_time <= epoch_end_date:
				queue_length = queue_length + 1

		# 4. flow_rate, # number (people seen in last hour)
		# calculations done in seconds
		epoch_one_hour_ago = (current_time/1000) - 3600
		seen_queue = self.firebaseManager.get_patients_seen()

		if is_walk_in:
			doctor_name = 'walk_in'

		flow_rate = 0
		for user in seen_queue:
			if user.get('doctor') == doctor_name:
				seen_time = user.get('seen_time')
				if seen_time >= epoch_one_hour_ago and seen_time <= current_time:
					flow_rate = flow_rate + 1

		# 1. arrival_time, # number (minutes since 00:00)
		arrival_time = ((current_time/1000) - epoch_start_date)/60

		# 5. doctor, # string ('a', 'b', 'c', etc.)
		if doctor_name == 'doctor_hudson':
			doctor = 'c'
		elif doctor_name == 'doctor_martin':
			doctor = 'i'
		else:
			# walk_in
			doctor = 'g'

		# 6. appointment_time, # number (minutes since 00:00)
		# use appointment_time
		if is_walk_in:
			appointment_time = arrival_time
		else:
			appointment_time = ((appointment_time/1000) - epoch_start_date)/60

		# 7. isWalkIn, # boolean
		# use is_walk_in

		# print some stuff out
		print("---")
		print("arrival_time: " + str(arrival_time))
		print("weekday: " + weekday)
		print("flow_rate: " + str(flow_rate))
		print("queue_length: " + str(queue_length))
		print("doctor: " + doctor_name)
		print("appointment_time: " + str(appointment_time))
		print("is_walk_in: " + str(is_walk_in))

		estimate = estimateWaitTime(arrival_time, weekday, flow_rate, queue_length, doctor, appointment_time, is_walk_in)

		# print some stuff out
		print("estimated wait time: " + str(estimate))

		estimate = estimate*60*1000 + current_time

		# print some stuff out
		print("estimated time: " + str(estimate))

		return estimate

	# helper function to get epoch current millis
	def get_current_millis(self):
		return int(round(time.time() * 1000))