import time

from pprint import pprint
from FirebaseManager import FirebaseManager
from DatabaseManager import DatabaseManager
from Residual import Residual
from rmodel import estimateWaitTime

class QueueManager:
	def __init__(self):
		self.firebaseManager = FirebaseManager()
		self.databaseManager = DatabaseManager()
		self.users = {}
		self.residuals = {}

		self.cache_users()

	# store residual
	def store_residual(self, user_id, seen_time_millis):
		seen_time_sec = seen_time_millis/1000

		user_id_key = str(user_id)
		residual = self.residuals.get(user_id_key, None)

		# timestamp
		residual.timestamp = seen_time_millis

		# calculate seen time = minutes, 0 being 12:00AM
		date = time.strftime("%m/%d/%Y", time.localtime(seen_time_sec))
		epoch_start_date = int(time.mktime(time.strptime(date, "%m/%d/%Y"))) # start time of day in seconds
		seen_time = int((seen_time_sec - epoch_start_date)/60)
		residual.seen_time = seen_time

		if residual:
			self.databaseManager.store_residual(residual)
			del self.residuals[user_id_key]

	# get all users from db and store locally
	def cache_users(self):
		db_users = self.firebaseManager.get_users()
		if not db_users:
			return
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

		if queue is None:
			queue = []
			queue.append(data)
		elif scheduled_start_time >= queue[-1]['scheduled_start_time']:
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

		# log
		self.databaseManager.log("add to scheduled: " + str(user_id) + " - " + name
			+ " for " + doctor_name
			+ " at " + str(scheduled_start_time))

	# logic for walk in check in
	def add_walk_in(self, user_id, name, current_time=-1):
		if current_time < 0:
			current_time = self.get_current_millis()
		predicted_wait_time_min, predicted_wait_time_max = self.get_new_model_prediction(user_id, arrival_time_millis=current_time)
		queue = self.firebaseManager.get_walk_in_queue()
		length = 0
		if queue:
			length = len(queue)
			for user in queue:
				if user.get('id') and user.get('id') == user_id:
					return False
		self.firebaseManager.add_walk_in_user(length, user_id, name, current_time, predicted_wait_time_min, predicted_wait_time_max)
		self.firebaseManager.add_user(user_id, name)
		self.cache_users()

		# log
		self.databaseManager.log("add to walk in: " + str(user_id) + " - " + name)

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
			#predicted_wait_time = self.get_predicted_start_time(current_time, False, doctor, user.get('scheduled_start_time'), user_id)
			self.firebaseManager.check_in_scheduled_user(doctor, user_index, current_time, -1, -1)

			# log
			self.databaseManager.log("check in scheduled: " + str(user_id))

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
			paging_queue = self.firebaseManager.get_now_paging()
			queue_size = 0 if paging_queue is None else len(paging_queue)

			# add user to now_paging
			self.firebaseManager.add_paging_user(queue_size, user)

			# remove user from current queue
			del queue[index]
			self.firebaseManager.update_queue(doctor, queue)

			# log
			self.databaseManager.log("page: " + str(user_id) + " to " + str(room))

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
			patients_seen_queue = self.firebaseManager.get_patients_seen()
			queue_size = 0 if patients_seen_queue is None else len(patients_seen_queue)
			current_time_millis = self.get_current_millis()
			user['seen_time'] = current_time_millis
			self.firebaseManager.add_seen_user(queue_size, user)

			# remove user from now_paging
			del users[index]
			self.firebaseManager.update_now_paging(users)

			# store residual
			self.store_residual(user_id, current_time_millis)

			# log
			self.databaseManager.log("seen: " + str(user_id))

	# new prediction model, should only be used for walk in
	def get_new_model_prediction(self, user_id, arrival_time_millis=-1):
		# to ensure only for walk in
		is_walk_in = True

		# this allows for us to manually input arrival times for prototype demo
		if arrival_time_millis < 0:
			arrival_time_millis = self.get_current_millis()

		arrival_time_sec = arrival_time_millis/1000

		date = time.strftime("%m/%d/%Y", time.localtime(arrival_time_sec))
		epoch_start_date = int(time.mktime(time.strptime(date, "%m/%d/%Y"))) # start time of day in seconds
		epoch_end_date = epoch_start_date + (60*60*24 - 1) # end time of day in seconds

		# 1. arrival_time, # number (minutes since 00:00)
		arrival_time = (arrival_time_sec - epoch_start_date)/60 # in minutes

		# 2. weekday, # string ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
		weekday = time.strftime("%A", time.localtime(arrival_time_sec))
		weekday = weekday.lower()[:3]

		# 3. flow_rate, # number (people seen in last hour), calculations done in seconds
		epoch_one_hour_ago = (arrival_time_sec) - (60*60)
		seen_queue = self.firebaseManager.get_patients_seen()

		if is_walk_in:
			doctor_name = 'walk_in'

		flow_rate = 0
		if seen_queue:
			for user in seen_queue:
				if user.get('doctor') == doctor_name:
					seen_time = user.get('seen_time')/1000
					if seen_time >= epoch_one_hour_ago and seen_time <= arrival_time_sec:
						flow_rate = flow_rate + 1

		# 4. queue_length, # number
		if is_walk_in:
			queue = self.firebaseManager.get_walk_in_queue()
		else:
			queue = self.firebaseManager.get_doctor_queue(doctor_name)

		queue_length = 0
		if queue:
			for user in queue:
				if user.get('id') == user_id:
					break
				queue_length = queue_length + 1

		# 5. doctor
		doctor = 0

		# 6. appointment_time
		appointment_time = -1

		# 7. num_doctors
		num_doctors = 1

		# 8. month [1-12] int (1 for jan, 12 for dec)
		month_as_str = time.strftime("%b", time.localtime(arrival_time_sec))
		month = time.strptime(month_as_str, '%b').tm_mon

		# hardcoded because 'sun' does not work
		weekday = 'mon'

		estimate = estimateWaitTime(arrival_time, weekday, flow_rate, queue_length, doctor, appointment_time, is_walk_in, num_doctors, month)
		print(estimate)
		print(arrival_time, weekday, flow_rate, queue_length, doctor, appointment_time, is_walk_in, num_doctors, month)

		# defaults
		lower_bound = arrival_time_millis + 1000*60*30
		upper_bound = arrival_time_millis + 1000*60*45
		estimated_wait_time = 38

		if len(estimate) >= 2:
			# convert to millis
			lower_bound = estimate[0]*60*1000 + arrival_time_millis
			upper_bound = estimate[1]*60*1000 + arrival_time_millis
			estimated_wait_time = int(estimate[2])

		# store residual
		residual = Residual(
			arrival_time,
			weekday,
			flow_rate,
			queue_length,
			doctor,
			is_walk_in,
			num_doctors,
			month,
			estimated_wait_time)
		self.residuals[str(user_id)] = residual

		return lower_bound, upper_bound

	# DEPRECATED
	# helper function to get predicted start time from prediction model
	def get_predicted_start_time(self, current_time, is_walk_in, doctor_name, appointment_time, user_id):
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
		# below is wrong...this just gets queue size within the day...
		# for user in queue:
		# 	if is_walk_in:
		# 		queue_time = user.get('check_in_time')/1000
		# 	else:
		# 		queue_time = user.get('scheduled_start_time')/1000

		# 	if queue_time >= epoch_start_date and queue_time <= epoch_end_date:
		# 		queue_length = queue_length + 1

		# correct way of getting queue_length
		queue_length = 0
		if queue:
			for user in queue:
				if user.get('id') == user_id:
					break
				queue_length = queue_length + 1

		# 4. flow_rate, # number (people seen in last hour)
		# calculations done in seconds
		epoch_one_hour_ago = (current_time/1000) - 3600
		seen_queue = self.firebaseManager.get_patients_seen()

		if is_walk_in:
			doctor_name = 'walk_in'

		flow_rate = 0

		if seen_queue:
			for user in seen_queue:
				if user.get('doctor') == doctor_name:
					seen_time = user.get('seen_time')
					if seen_time >= epoch_one_hour_ago*1000 and seen_time <= current_time:
						flow_rate = flow_rate + 1

		# 1. arrival_time, # number (minutes since 00:00)
		arrival_time = ((current_time/1000) - epoch_start_date)/60

		# 5. doctor, # string ('a', 'b', 'c', etc.)
		if doctor_name == 'doctor_hudson':
			doctor = 'n'
		elif doctor_name == 'doctor_martin':
			doctor = 'e'
		else:
			# walk_in
			doctor = 'a'

		# 6. appointment_time, # number (minutes since 00:00)
		# use appointment_time
		if is_walk_in:
			appointment_time = arrival_time
		else:
			appointment_time = ((appointment_time/1000) - epoch_start_date)/60

		# 7. isWalkIn, # boolean
		# use is_walk_in

		### hardcoding ###
		flow_rate = 5
		if not is_walk_in:
			arrival_time = appointment_time - 5

		# print some stuff out
		# print("---")
		# print("arrival_time: " + str(arrival_time))
		# print("weekday: " + weekday)
		# print("flow_rate: " + str(flow_rate))
		# print("queue_length: " + str(queue_length))
		# print("doctor: " + doctor_name)
		# print("appointment_time: " + str(appointment_time))
		# print("is_walk_in: " + str(is_walk_in))

		estimate = estimateWaitTime(arrival_time, weekday, flow_rate, queue_length, doctor, appointment_time, is_walk_in)

		# print some stuff out
		# print("estimated wait time: " + str(estimate))

		estimate = estimate*60*1000 + current_time

		# print some stuff out
		# print("estimated time: " + str(estimate))

		return estimate

	# helper function to get epoch current millis
	def get_current_millis(self):
		return int(round(time.time() * 1000))