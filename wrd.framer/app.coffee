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

pagingSound = new Audio("sounds/paging_sound.mp3")

round5 = (x) ->
	return Math.ceil(x/5)*5;

renderNowCallingPatients = (patients) ->
	nowCallingHeader = new TextLayer
		parent: nowCalling
		text: "Now Calling"
		fontWeight: 800
		fontSize: 64
		color: 'white'
		x: Align.center
		fontFamily: Utils.loadWebFont "Nunito Sans"

	if patients == null or patients == undefined
		patients = []
	for patient,i in patients
		nowCallingPatient = new Layer
			width: 420
			height: 175
			backgroundColor: 'transparent'
			borderRadius: 12
			x: Align.center
			y: 150 + i * 195
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
			x: Align.center
			y: Align.center

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

bg = new Layer
	backgroundColor: 'white'
	width: 1400
	height: 1080
	x: 520

displayHeader = new TextLayer
	fontFamily: Utils.loadWebFont "Nunito Sans"
	text: 'Estimated Wait Times'
	fontSize: 64
	parent: bg
	x: 80
	fontWeight: 700
	color: "#47525D"
	y: 55

dividerh = new Layer
	width: bg.width
	height: 2
	backgroundColor: "#D8D8D8"
	parent: bg
	y: 180

dividerh = new Layer
	width: bg.width
	height: 2
	backgroundColor: "#D8D8D8"
	parent: bg
	y: 300

dividerv = new Layer
	width: 2
	height: bg.height
	backgroundColor: "#D8D8D8"
	parent: bg
	y: 180
	x: bg.width/3

dividerv = new Layer
	width: 2
	height: bg.height
	backgroundColor: "#D8D8D8"
	parent: bg
	y: 180
	x: 2*bg.width/3

tagline = new TextLayer
	fontFamily: Utils.loadWebFont "Nunito Sans"
	text: 'These are estimated wait times, we appreciate your patience!'
	fontSize: 32
	parent: bg
	x: Align.center
	color: "#47525D"
	y: bg.height - 80

patientLists = new Layer
	width: bg.width
	parent: bg
	x: Align.center
	y: 230
	backgroundColor: 'transparent'
	height: 608

nowCalling = new Layer
	width: 520
	y: 50
	backgroundColor: 'transparent'

renderList = (listPos, header, patients, isWalkIn = false) ->
	list = new Layer
		width: 360
		y: 0
		height: 608
		backgroundColor: 'transparent'
		parent: patientLists
		x: 53 + listPos * 463

	listHeader = new TextLayer
		parent: list
		text: header
		fontWeight: 800
		fontSize: 32
		color: '#47525D'
		fontFamily: Utils.loadWebFont "Nunito Sans"

	if patients == null or patients == undefined
		patients = []

	patientsToDisplay = []
	for patient,i in patients
		if isWalkIn is true or patient.is_checked_in is true
			patientsToDisplay.push(patient)

	for patient,i in patientsToDisplay
		print(patient.name, patient.is_checked_in)
		if isWalkIn is true
			bgColor = "#F4E7FF"
			nameColor = "#AF6CD5"
			waitColor = "#877A87"
			borderColor = "#F4E7FF"
			maxWaitTime = (patient.predicted_start_time_max - (new Date).getTime())/60000
			minWaitTime = (patient.predicted_start_time_min - (new Date).getTime())/60000
			detail = round5(minWaitTime) + '-' + round5(maxWaitTime) + " min"

		if patient.is_checked_in is true 
			print('here')
			bgColor = "#DAE7FF"
			nameColor = "#4786FF"
			waitColor = "#7A7C87"
			borderColor = "#DAE7FF"
			apptTime = new Date(patient.predicted_start_time);
			hours = apptTime.getHours()
			if hours >= 12
				ampm = 'PM'
			else
				ampm = 'AM'
			hours = hours % 12;
			hours = hours ? hours : 12;
			detail = "Scheduled at " + hours + ":" + apptTime.getMinutes() + ' ' + ampm

		if isWalkIn is true or patient.is_checked_in is true 
			patientCard = new Layer
				width: 360
				height: 138
				backgroundColor: bgColor
				borderRadius: 12
				y: 120 + 158 * i
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

			detail = new TextLayer
				text: detail
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
	old_length = nowCalling.children.length
	for child in nowCalling.children
		child.destroy()
	firebase.get "/now_paging", (queue) ->
		renderNowCallingPatients(queue)
		new_length = nowCalling.children.length
		if new_length > old_length
			pagingSound.play()

renderAllQueues = ->
	firebase.get "/queues", (queues) ->
		now = new Date()
		today = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0)
		tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 0)

		martinPatients = if queues and queues.doctor_martin then queues.doctor_martin.filter (p) -> p.scheduled_start_time > today.valueOf() and p.scheduled_start_time < tomorrow.valueOf() else []
		hudsonPatients = if queues and queues.doctor_hudson then queues.doctor_hudson.filter (p) -> p.scheduled_start_time > today.valueOf() and p.scheduled_start_time < tomorrow.valueOf() else []
		walkInPatients = if queues and queues.walk_in then queues.walk_in else []
		
		
		martinPatients = if queues and queues.doctor_martin then queues.doctor_martin else []
		hudsonPatients = if queues and queues.doctor_hudson then queues.doctor_hudson else []
		renderList(0, "Walk-in Appointments", walkInPatients, true)
		renderList(1, "Dr. Martin's Schedule", martinPatients)
		renderList(2, "Dr. Hudson's Schedule", hudsonPatients)

setInterval () ->
		renderAllQueues()
	,60*1000
