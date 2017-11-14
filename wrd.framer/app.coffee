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

renderNowCallingPatients = (patients) ->
	nowCalling = new Layer
		width: 520
		y: 301
		backgroundColor: 'transparent'
		
	nowCallingHeader = new TextLayer
		parent: nowCalling
		text: "Now Calling"
		fontWeight: 800
		fontSize: 48
		color: 'white'
		x: 50
		fontFamily: Utils.loadWebFont "Nunito Sans"

	for patient,i in patients
		nowCallingPatient = new Layer
			width: 420
			height: 175
			backgroundColor: 'rgba(255, 255, 255, 0.5)'
			borderRadius: 12
			x: Align.center
			y: 85 + i * 195
			parent: nowCalling
			
		patientName = new TextLayer
			text: patient[0]
			parent: nowCallingPatient
			fontFamily: Utils.loadWebFont "Nunito Sans"
			fontWeight: 700
			fontSize: 42
			color: "#47525D"
			x: 50
			y: 35
		
		patientRoom = new TextLayer
			text: patient[1]
			parent: nowCallingPatient
			fontFamily: Utils.loadWebFont "Nunito Sans"
			fontWeight: 700
			fontSize: 32
			color: "#47525D"
			x: 50
			y: 102

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

renderDate = (today) ->
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
	if today.getDay() is 1
		day = today.getDay() + "st"
	else if today.getDate is 2
		day = today.getDay() + "nd"
	else
		day = today.getDay() + "th"
	daylist[today.getDay()] + ", " + monthlist[today.getMonth()] + " " + day
	
renderTime = (today) ->
	if today.getHours() > 12
		today.getHours() - 12 + ":" + ("00" + today.getMinutes()).slice(2)
	else
		today.getHours() + ":" + today.getMinutes()

renderMeridian = (today) ->
	if today.getHours() > 12
		"PM"
	else
		"AM"

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

time = new TextLayer
	parent: sidebar
	text: today.getHours() + ":" + today.getMinutes()
	fontSize: 130
	textAlign: "left"
	fontWeight: 100
	color: 'white'
	x: 50
	fontFamily: Utils.loadWebFont "Nunito Sans"
	y: 104

meridian = new TextLayer
	parent: time
	text: renderMeridian(today)
	x: time.width
	y: 80
	color: 'white'

patients = [["T.Flenderson", "Room 1"], ["M. Scott", "Room 2"]]
renderNowCallingPatients(patients)

