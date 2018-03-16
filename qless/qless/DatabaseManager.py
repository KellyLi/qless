import sqlite3
import time

class DatabaseManager:
	def __init__(self):
		print("DatabaseManager Initialized...")

	def get_connection(self):
		sqlite_file = 'database/qless.db'
		connection = sqlite3.connect(sqlite_file)
		return connection

	def log(self, description):
		connection = self.get_connection()
		c = connection.cursor()

		try:
			c.execute("INSERT INTO log (description, time) VALUES (?, ?)", (description, self.get_current_millis()))
			print("logged: " + description)
		except Exception as e:
			print(e)
			print("log failed: " + description)

		connection.commit()
		connection.close()

	# helper function to get epoch current millis
	def get_current_millis(self):
		return int(round(time.time() * 1000))
