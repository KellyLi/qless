import sys
sys.path.insert(0, '../qless/')

from QueueManager import QueueManager
from FirebaseManager import FirebaseManager

firebaseManager = FirebaseManager()

# clear firebase data
def clear_data():
	firebaseManager.update_queue("walk_in", [])
	firebaseManager.update_queue("doctor_hudson", [])
	firebaseManager.update_queue("doctor_martin", [])
	firebaseManager.update_now_paging([])
	firebaseManager.update_seen_users([])
	firebaseManager.update_users([])

#############################################
# 	run functions here to populate data 	#
#############################################
clear_data()