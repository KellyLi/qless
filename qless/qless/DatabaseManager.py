import sqlite3
import time

class DatabaseManager:
	def __init__(self):
		print("DatabaseManager Initialized...")

	def get_connection(self):
		sqlite_file = 'database/qless.db'
		try:
			connection = sqlite3.connect(sqlite_file)
		except:
			return None
		return connection

	def log(self, description):
		connection = self.get_connection()

		if connection is None:
			print("log: couldn't connect to sqlite3")
			return

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
