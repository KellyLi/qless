# Define and set custom device
Framer.Device.customize
	devicePixelRatio: 1
	screenWidth: 1920
	screenHeight: 1080
	deviceImageWidth: 1920
	deviceImageHeight: 1080

{Firebase} = require "firebase/firebase"

firebase = new Firebase
	projectID: "qless-74979"
	secret: "V1PiKsbNoepuy6aXxinccYyvt08pQYanjlAzd7Gn"

renderNowCallingPatients = (patients) ->
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
			backgroundColor: 'transparent'
			borderRadius: 12
			x: Align.center
			y: 85 + i * 195
			parent: nowCalling

		nowCallingPatientFade = new Layer
			width: 420
			height: 175
			backgroundColor: '#fff'
			borderRadius: 12
			opacity: .6
			parent: nowCallingPatient

		patientName = new TextLayer
			text: patient.name
			parent: nowCallingPatient
			fontFamily: Utils.loadWebFont "Nunito Sans"
			fontWeight: 700
			fontSize: 42
			color: "#47525D"
			x: 50
			y: 35

		patientRoom = new TextLayer
			text: patient.room
			parent: nowCallingPatient
			fontFamily: Utils.loadWebFont "Nunito Sans"
			fontWeight: 700
			fontSize: 32
			color: "#47525D"
			x: 50
			y: 102

		fadeIn  = new Animation nowCallingPatientFade,
			opacity: .8
			scale: 1.02

		fadeOut = fadeIn.reverse()

		# Alternate between the two animations
		fadeIn.on Events.AnimationEnd, fadeOut.start
		fadeOut.on Events.AnimationEnd, fadeIn.start

		fadeIn.start()

sidebar  = new Layer
	width: 320
	height: 1080

# Create layer, define image
layer = new Layer
	parent: sidebar
	width: 520
	height: 1080
	image: "images/sidebar_bg.jpg"

renderDate = (today) ->
	daylist = [
		'Sunday'
		'Monday'
		'Tuesday'
		'Wednesday'
		'Thursday'
		'Friday'
		'Saturday'
	]

	monthlist = [
		'Jan'
		'Feb'
		'Mar'
		'Apr '
		'May'
		'Jun'
		'Jul',
		'Aug',
		'Sept',
		'Oct',
		'Nov',
		'Dec'
	]

	if today.getDate() is 1 or today.getDate() is 21
		day = today.getDate() + "st"
	else if today.getDate() is 2 or today.getDate() is 22
		day = today.getDate() + "nd"
	else if today.getDate() is 3 or 13 or today.getDate() is 23
		day = today.getDate() + "rd"
	else
		day = today.getDate() + "th"
	daylist[today.getDay()] + ", " + monthlist[today.getMonth()] + " " + day

renderTime = (today) ->
	if today.getHours() > 12
		("00" + (today.getHours() - 12)).slice(-2) + ":" + ("00" + today.getMinutes()).slice(-2)
	else
		("00" + (today.getHours() - 12)).slice(-2)+ ":" + ("00" + today.getMinutes()).slice(-2)

renderMeridian = (today) ->
	if today.getHours() > 12
		"PM"
	else
		"AM"

now = new Date
time = new TextLayer
	parent: sidebar
	text: renderTime(now)
	fontSize: 130
	textAlign: "left"
	fontWeight: 100
	color: 'white'
	x: 50
	fontFamily: Utils.loadWebFont "Nunito Sans"
	y: 104
	width: 340

meridian = new TextLayer
	parent: time
	text: renderMeridian(now)
	x: time.width
	y: 80
	color: 'white'

updateClock = ->
	now = new Date
	time.text = renderTime(now)
	meridian.text = renderMeridian(now)

date = new TextLayer
	parent: sidebar
	text: renderDate(new Date)
	fontSize: 40
	width: 520
	textAlign: "left"
	fontWeight: 500
	color: 'white'
	x: 50
	fontFamily: Utils.loadWebFont "Nunito Sans"
	y: 50

bg = new Layer
	backgroundColor: 'white'
	width: 1400
	height: 1080
	x: 520

clinicName = new TextLayer
	fontFamily: Utils.loadWebFont "Nunito Sans"
	text: 'Silver Oak Medical Centre'
	fontSize: 64
	parent: bg
	x: 80
	fontWeight: 700
	color: "#47525D"
	y: 55

tagline = new TextLayer
	fontFamily: Utils.loadWebFont "Nunito Sans"
	text: 'These are estimated wait times, we appreciate your patience!'
	fontSize: 32
	parent: bg
	x: 80
	color: "#47525D"
	y: 153

divider = new TextLayer
	width: 145
	height: 6
	backgroundColor: "#E6E7E9"
	parent: bg
	y: 236
	x: 80

patientLists = new Layer
	width: 1241
	parent: bg
	x: Align.center
	y: 282
	backgroundColor: 'transparent'
	height: 608

nowCalling = new Layer
	width: 520
	y: 301
	backgroundColor: 'transparent'

renderList = (listPos, header, subtitle, patients, isWalkIn = false) ->
	list = new Layer
		width: 360
		y: 0
		height: 608
		backgroundColor: 'transparent'
		parent: patientLists
		x: listPos * 440

	listHeader = new TextLayer
		parent: list
		text: header
		fontWeight: 800
		fontSize: 32
		color: '#47525D'
		fontFamily: Utils.loadWebFont "Nunito Sans"

	subtitle = new TextLayer
		parent: list
		text: subtitle
		fontWeight: 500
		fontSize: 32
		color: '#7B8994'
		fontFamily: Utils.loadWebFont "Nunito Sans"
		y: 49

	for patient,i in patients
		if isWalkIn is true
			bgColor = "#F4E7FF"
			nameColor = "#AF6CD5"
			waitColor = "#877A87"
			borderColor = "#F4E7FF"
			waitTime = (patient.predicted_start_time - (new Date).getTime())/60000
			formattedTime = Math.round(waitTime) + " min"
		else if patient.is_checked_in is true
			bgColor = "#DAE7FF"
			nameColor = "#4786FF"
			waitColor = "#7A7C87"
			borderColor = "#DAE7FF"
			waitTime = (patient.predicted_start_time - (new Date).getTime())/60000
			formattedTime = Math.round(waitTime) + " min"
		else if patient.is_checked_in is false
			bgColor = "#fff"
			nameColor = "#3D464D"
			waitColor = "#87807A"
			borderColor = "#EDEFF2"
			formattedTime = "not checked in"

		patientCard = new Layer
			width: 360
			height: 138
			backgroundColor: bgColor
			borderRadius: 12
			y: subtitle.y + subtitle.height + 40 + 158 * i
			parent: list
			borderColor: borderColor
			borderWidth: 2

		patientName = new TextLayer
			text: patient.name
			parent: patientCard
			fontFamily: Utils.loadWebFont "Nunito Sans"
			fontWeight: 700
			fontSize: 32
			color: nameColor
			x: 30
			y: 25

		patientWait = new TextLayer
			text: formattedTime
			parent: patientCard
			fontFamily: Utils.loadWebFont "Nunito Sans"
			fontWeight: 600
			fontSize: 28
			color: waitColor
			x: 30
			y: 75

firebase.onChange "/queues", ->
	for child in patientLists.children
		child.destroy()
	renderAllQueues()

firebase.onChange "/now_paging", ->
	for child in nowCalling.children
		child.destroy()
	firebase.get "/now_paging", (queue) ->
		renderNowCallingPatients(queue)

renderAllQueues = ->
	firebase.get "/queues", (queues) ->
		now = new Date()
		today = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0)
		tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 0)

		martinPatients = queues.doctor_martin.filter (p) -> p.scheduled_start_time > today.valueOf() and p.scheduled_start_time < tomorrow.valueOf()
		hudsonPatients = queues.doctor_hudson.filter (p) -> p.scheduled_start_time > today.valueOf() and p.scheduled_start_time < tomorrow.valueOf()
		renderList(0, "Walk-in Appointments","first come first serve", queues.walk_in, true)
		renderList(1, "Dr. Martin's Schedule","on time", martinPatients)
		renderList(2, "Dr. Hudson's Schedule","on time", hudsonPatients)

	updateClock()

setInterval () -> 
		renderAllQueues()
	,60*1000