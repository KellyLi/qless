class Residual:

	def __init__(self, 
		arrival_time, 
		weekday, 
		flow_rate, 
		queue_length, 
		doctor, 
		is_walk_in,
		num_doctors,
		month,
		estimated_wait_time):

		self.arrival_time = arrival_time				# minutes, 0 being 12:00AM
		self.weekday = weekday
		self.flow_rate = flow_rate
		self.queue_length = queue_length
		self.doctor = doctor
		self.is_walk_in = is_walk_in
		self.num_doctors = num_doctors
		self.month = month
		self.estimated_wait_time = estimated_wait_time	# minutes, 0 being 12:00AM [USE MEAN PROVIDED]

		# these residuals should always be this
		self.has_been_fitted = False					# will be set to True when model is fitted
		self.appt_time = -1								# minutes, 0 being 12:00AM

		# to be updated right before storing into sqlite3
		self.seen_time = -1
		self.timestamp = -1

# 	`arrival_time` INTEGER,
# 	`weekday` TEXT,
# 	`flow_rate` REAL,
# 	`queue_length` REAL,
# 	`doctor` INTEGER,
# 	`appt_time` INTEGER,
# 	`is_walk_in` REAL,
# 	`num_doctors` INTEGER,
# 	`month` INTEGER,
# 	`seen_time` INTEGER,
# 	`estimated_wait_time` REAL,
# 	`timestamp` INTEGER,
# 	`has_been_fitted` REAL