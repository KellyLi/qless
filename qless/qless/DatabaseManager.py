import sqlite3
import time
import os.path

LOG_MODE = False

class DatabaseManager:

	def __init__(self):
		self.package_dir = os.path.abspath(os.path.dirname(__file__))
		self.db_path = os.path.join(self.package_dir,'database/qless.db')

	def get_connection(self):
		try:
			connection = sqlite3.connect(self.db_path)
		except:
			return None
		return connection

	def log(self, description):
		if not LOG_MODE:
			return

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
