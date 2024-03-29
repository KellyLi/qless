import sys
sys.path.insert(0, '../qless/')

from QueueManager import QueueManager
from FirebaseManager import FirebaseManager

queueManager = QueueManager(sync_id_generators=False)
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

	queueManager.add_scheduled_user(0, "script_name_0", "doctor_hudson", (time + half_hour))
	queueManager.add_scheduled_user(1, "script_name_1", "doctor_hudson", (time + hour))
	queueManager.add_scheduled_user(2, "script_name_2", "doctor_hudson", (time + 1.5*hour))
	queueManager.add_scheduled_user(3, "script_name_3", "doctor_hudson", (time + 2*hour))
	print("	doctor_hudson users added")

	queueManager.add_scheduled_user(4, "script_name_4", "doctor_martin", (time + half_hour))
	queueManager.add_scheduled_user(5, "script_name_5", "doctor_martin", (time + 1.5*hour))
	queueManager.add_scheduled_user(6, "script_name_6", "doctor_martin", (time + 3*hour))
	queueManager.add_scheduled_user(7, "script_name_7", "doctor_martin", (time + 4*hour))
	print("	doctor_martin users added")

	print("populating scheduled users completed")

def populate_walk_in_users():
	print("populating walk in users...")

	# time is all in millis
	time = queueManager.get_current_millis()

	queueManager.add_walk_in(8, "script_name_8", current_time=time - half_hour);
	queueManager.add_walk_in(9, "script_name_9", current_time=time - 0.5*half_hour);

	print("populating walk in users completed")

def check_in_scheduled_users():
	print("checking in scheduled users...")
	queueManager.check_in_scheduled(0)
	queueManager.check_in_scheduled(1)
	queueManager.check_in_scheduled(2)
	queueManager.check_in_scheduled(3)
	queueManager.check_in_scheduled(4)
	queueManager.check_in_scheduled(5)
	queueManager.check_in_scheduled(6)
	queueManager.check_in_scheduled(7)
	print("checking scheduled users completed")

def page_walk_in_users():
	print("paging walk in users...")
	queueManager.page_user(8, "Room A")
	print("paging walk in users completed")

def seen_walk_in_users():
	print("set seen walk in users...")
	queueManager.seen_user(8)
	print("set seen walk in users completed")


###############################################
#     run functions here to populate data     #
###############################################
print("running populate_demo_data...")

clear_data()

populate_scheduled_users()
check_in_scheduled_users()

populate_walk_in_users()
page_walk_in_users()
seen_walk_in_users()

print("populate_demo_data completed!")