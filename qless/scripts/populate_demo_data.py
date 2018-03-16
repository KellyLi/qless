import sys
sys.path.insert(0, '../qless/')

from QueueManager import QueueManager
from FirebaseManager import FirebaseManager

queueManager = QueueManager()
firebaseManager = FirebaseManager()

# time is all in millis
hour = 1000*60*60
half_hour = 1000*60*30

# clear firebase data
def clear_data():
	print("clearing all data...")
	firebaseManager.update_queue("walk_in", [])
	print("	walk_in cleared")
	firebaseManager.update_queue("doctor_hudson", [])
	print("	doctor_hudson queue cleared")
	firebaseManager.update_queue("doctor_martin", [])
	print("	doctor_martin queue cleared")
	firebaseManager.update_now_paging([])
	print("	now paging cleared")
	firebaseManager.update_seen_users([])
	print("	seen users cleared")
	firebaseManager.update_users([])
	print("	users cleared")
	print("all data cleared")

def populate_scheduled_users():
	print("populating scheduled users...")

	# time is all in millis
	time = queueManager.get_current_millis()

	queueManager.add_scheduled_user(0, "H1", "doctor_hudson", (time + half_hour))
	queueManager.add_scheduled_user(1, "H2", "doctor_hudson", (time + hour))
	queueManager.add_scheduled_user(2, "H3", "doctor_hudson", (time + 1.5*hour))
	queueManager.add_scheduled_user(3, "H4", "doctor_hudson", (time + 2*hour))
	print("	doctor_hudson users added")

	queueManager.add_scheduled_user(4, "M1", "doctor_martin", (time + half_hour))
	queueManager.add_scheduled_user(5, "M2", "doctor_martin", (time + 1.5*hour))
	queueManager.add_scheduled_user(6, "M3", "doctor_martin", (time + 3*hour))
	queueManager.add_scheduled_user(7, "M3", "doctor_martin", (time + 4*hour))
	print("	doctor_martin users added")

	print("populating scheduled users completed")

def populate_walk_in_users():
	print("populating walk in users...")

	time = queueManager.get_current_millis()

	queueManager.add_walk_in(8, "W1", current_time=time - half_hour);
	queueManager.add_walk_in(9, "W2", current_time=time - 0.5*half_hour);
	queueManager.add_walk_in(10, "W3", current_time=time);

	print("populating walk in users completed")

###############################################
#     run functions here to populate data     #
###############################################
clear_data()
populate_scheduled_users()
populate_walk_in_users()