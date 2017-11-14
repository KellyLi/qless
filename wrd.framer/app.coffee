# Define and set custom device
Framer.Device.customize
	devicePixelRatio: 1
	screenWidth: 1920
	screenHeight: 1080

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

sidebar  = new Layer
	width: 320
	height: 1080

# Create layer, define image
layer = new Layer
	parent: sidebar
	width: 520
	height: 1080
	image: "images/sidebar_bg.jpg"

today = new Date

daylist = [  
  'Sunday'  
  'Monday'  
  'Tuesday'  
  'Wednesday '  
  'Thursday'  
  'Friday'  
  'Saturday'  
]

monthlist = [  
  'January'  
  'Feburary'  
  'March'  
  'April '  
  'May'  
  'June'  
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]

renderDate = (today) ->
	if today.getDay() is 1
		day = today.getDay() + "st"
	else if today.getDate is 2
		day = today.getDay() + "nd"
	else
		day = today.getDay() + "th"
	daylist[today.getDay()] + ", " + monthlist[today.getMonth()] + " " + day
	
renderTime = (today) ->
	if today.getHours() > 12
		today.getHours() - 12 + ":" + today.getMinutes() + "PM"
	else
		today.getHours() + ":" + today.getMinutes() + "AM" 

date = new TextLayer
	parent: sidebar
	text: renderDate(today)
	fontSize: 40
	width: 520
	textAlign: "left"
	fontWeight: 500
	color: 'white'
	x: 50
	fontFamily: Utils.loadWebFont "Nunito Sans"
	y: 50

clock = new TextLayer
	parent: sidebar
	text: today.getHours() + ":" + today.getMinutes()
	fontSize: 130
	width: 520
	textAlign: "left"
	fontWeight: 100
	color: 'white'
	x: 50
	fontFamily: Utils.loadWebFont "Nunito Sans"
	y: 104

nowCalling = new TextLayer
	parent: sidebar
	text: "Now Calling"
	fontWeight: 800
	fontSize: 48
	color: 'white'
	x: 50
	y: 301
	fontFamily: Utils.loadWebFont "Nunito Sans"

