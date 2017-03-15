import database, twiliow, json, recieve, datetime, time

class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM users where name='{}' LIMIT 1".format(name)
		return database.get_row(query)
		
	def addPerson(model, request):
		person = request["person"]
		print person
		return database.insertObj(person, "users")

	def getPeople(model, request):
		query = "SELECT userId, name, pic, email FROM users"
		return database.get_results(query)

	def sendTxt(model, request):
		fromUser = request['username']
		authToken = request['authToken']
		tooUser = request["name"]
		meeting = request["type"]
		fromQuery = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(fromUser))
		toQuery = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(tooUser))
		if(fromQuery['authToken'] == str(authToken)):
			if(twiliow.MessageUser(toQuery['telephone'], meeting, fromUser)):
				return {"true":"awsome"}
		else:
			return {"error":"failed to authenticate"}


	def Auth(modle, request):
		name = request["name"]
		authToken = request['authToken']
		query = "SELECT * FROM users where name='{}' LIMIT 1".format(name)
		result = database.get_row(query)
		if(result != {"error" : "Object Not Found"}):
			if(result['authToken'] == authToken):
				return {"true":"user is valid"}
			else:
				return {"error":"invalid authToken"}
		else:
			return {"true":"user not found"}

	def test(model, request):
		waitTime = 0
		fromUserName = request['username']
		toUserName = request["name"]
		meeting = request["meeting"]
		fromQuery = "SELECT * FROM users where name='{}' LIMIT 1".format(fromUserName)
		toQuery = "SELECT * FROM users where name='{}' LIMIT 1".format(toUserName)
		toUser = database.get_row(toQuery)
		fromUser = database.get_row(fromQuery)
		checkQuery = "SELECT * FROM requests WHERE fromUserId='{}' AND Status='Active' LIMIT 1".format(fromUser['userId'])
		print checkQuery
		result = database.get_results(checkQuery)
		
		if not result:
			noReqs = True
		else:
			checkTimeStamp = database.get_row(checkQuery)
			currentTime = int(time.time())
			waitTime = int(checkTimeStamp['time']) + 300 - currentTime
			#loggedTime = datetime.datetime.strptime(checkTimeStamp['time'][:-6], '%Y-%m-%d %H:%M:%S')
			if checkTimeStamp['Status'] == "Active":
				if currentTime > int(checkTimeStamp['time']) + 300:
					updateLog = "UPDATE requests SET Status='Closed' where requestId='{}'".format(checkTimeStamp['requestId'])
					database.executeSQL(updateLog)
					noReqs = True
				else:
					noReqs = False
					
			else:
				noReqs = False
		if(noReqs):
			twiliowResp = twiliow.MessageUser(toUser['telephone'], meeting, fromUser['name'])
			if(twiliowResp[0]):
				logRequest =  {
					"fromUserId": fromUser['userId'],
					"Status":str("Active"),
					"toUserId": toUser['userId'],
					"time":int(time.time()),
					"responded":"false",
					"twilioMessageSid": twiliowResp[1],
					"metaDataJSON":request
				}	
				database.insertObj(logRequest, "requests")
				return {"Sucsess":"message sent"}
			else:
				return twiliowResp[0]
		else:
			return {"error":"please wait till teacher responds or ticket expires "+ str(waitTime)}
		#print database.insertObj(logRequest, "requests")
		
		
	def MessageResponse(model, request):
		number = request["From"][0].split('+')[1]
		print number
		findFromUser = "SELECT * FROM users where telephone='{}' LIMIT 1".format(number)
		usercheck = database.get_row(findFromUser)
		try:
			checkRequest = "SELECT * FROM requests where toUserId='{}' and Status='Active' LIMIT 1".format(usercheck['userId'])
			check = database.get_row(checkRequest)
			if check['responded'] == "false":
				id = "SELECT * FROM users where userId='{}' LIMIT 1".format(check['fromUserId'])
				pulluser = database.get_row(id)
				response = twiliow.Notify(str(pulluser['telephone']), usercheck['name'], request["Body"][0])
				updateLogs = "UPDATE requests SET Status='Closed', responded='true', response='{}' where requestId='{}'".format(request["body"][0],check['requestId'])
				print updateLogs
				database.executeSQL(updateLogs)
		except ValueError as e:
			print e
