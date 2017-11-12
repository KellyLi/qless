{Firebase} = require "firebase/firebase"

currentTime = (new Date).getTime();
currentTime = 1510509330; #delete this

firebase = new Firebase
	projectID: "qless-74979"
	secret: "V1PiKsbNoepuy6aXxinccYyvt08pQYanjlAzd7Gn"

firebase.get "/", (value) ->
	patientList = value
	for patient in patientList
		print patient.name
		print patient.appointment_start - currentTime
