import subprocess
import os

dir = os.path.dirname(__file__)

COMMAND = 'Rscript'
PATH = 'predictFromModel.R'

def estimateWaitTime(
		arrival_time, # number (minutes since 00:00)
		weekday, # string ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
		flow_rate, # number (people seen in last hour)
		queue_length, # number
		doctor, # string ('a', 'b', 'c', etc.)
		appointment_time, # number (minutes since 00:00)
		isWalkIn, # boolean
	):
	args = [str(arrival_time), str(weekday), str(flow_rate), str(queue_length),
			str(doctor), str(appointment_time), str(int(isWalkIn))]
	cmd = [COMMAND, PATH] + args
	result = subprocess.check_output(cmd, universal_newlines=True, cwd=dir)
	return float(result.split(' ')[-1].strip())
