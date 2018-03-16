import subprocess
import os

dir = os.path.dirname(__file__)

COMMAND = 'Rscript'
PATH = 'predictFromModel.R'

def estimateWaitTime(
		arrival_time, # int (minutes since 00:00)
		weekday, # string ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
		flow_rate, # int (people seen in last hour)
		queue_length, # int
		doctor, # int
		appointment_time, # int (minutes since 00:00)
		isWalkIn, # boolean
		num_doctors, # int
		month, # int (1 for jan, 12 for dec)
	):
	args = [str(arrival_time), str(weekday), str(flow_rate), str(queue_length),
			str(doctor), str(appointment_time), str(int(isWalkIn)),
 			str(num_doctors), str(month)]
	cmd = [COMMAND, PATH] + args
	result = subprocess.check_output(cmd, universal_newlines=True, cwd=dir)
	prediction = [float(pred.strip()) for pred in result.split(' ')[1:]
					if pred != '']
	return prediction
