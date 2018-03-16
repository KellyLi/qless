import sys
sys.path.insert(0, '../qless/')

from QueueManager import QueueManager
from FirebaseManager import FirebaseManager

queueManager = QueueManager()
firebaseManager = FirebaseManager()

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
	hour = 1000*60*60
	half_hour = 1000*60*30

	queueManager.add_scheduled_user(0, "K. Malone", "doctor_hudson", (time + half_hour))
	queueManager.add_scheduled_user(1, "P. Beesley", "doctor_hudson", (time + hour))
	queueManager.add_scheduled_user(2, "A. Balone", "doctor_hudson", (time + 1.5*hour))
	queueManager.add_scheduled_user(3, "C. Deesley", "doctor_hudson", (time + 2*hour))
	print("	doctor_hudson users added")

	queueManager.add_scheduled_user(4, "F. Galone", "doctor_martin", (time + half_hour))
	queueManager.add_scheduled_user(5, "H. Jeesley", "doctor_martin", (time + 1.5*hour))
	queueManager.add_scheduled_user(6, "K. Lalone", "doctor_martin", (time + 3*hour))
	queueManager.add_scheduled_user(7, "M. Neesley", "doctor_martin", (time + 4*hour))
	print("	doctor_martin users added")

	print("populating scheduled users completed")

###############################################
#     run functions here to populate data     #
###############################################
clear_data()
populate_scheduled_users()