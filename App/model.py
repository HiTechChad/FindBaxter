import database, twiliow, json, recieve, datetime, time, random, string
from gevent.pywsgi import WSGIServer
from twilio.rest import Client
class AppModel:
	def test(model, request):
		logRequest =  {
					"fromUserId": fromUser['userId'],
					"Status":str("Active"),
					"toUserId": toUser['userId'],
					"people":checkLogs[0]['count'],
					"time":int(time.time()),
					"responded":"false",
					"Response":" ",
					"twilioMessageSid": twiliowResp[1],
					"metaDataJSON":request
			}	
		print database.insertObj(logRequest, "requests")
	
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
	def SendMessage(model, request):
		waitTime = 0
		fromUserName = request['username']
		toUserName = request["name"]
		meeting = request["meeting"]
		toUser = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(toUserName))
		fromUser = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(fromUserName))
		checkQuery = "SELECT * FROM requests WHERE fromUserId='{}' AND Status='Active' LIMIT 1".format(fromUser['userId'])
		checkLogs = database.get_results("SELECT COUNT(*) as count FROM requests WHERE Status='Active' AND toUserId='{}'".format(toUser['userId']))
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
			twiliowResp = twiliow.MessageUser(toUser['telephone'], meeting, fromUser['name'], checkLogs[0]['count'])
			if(twiliowResp[0]):
				logRequest =  {
					"fromUserId": fromUser['userId'],
					"Status":str("Active"),
					"toUserId": toUser['userId'],
					"people":checkLogs[0]['count'],
					"time":int(time.time()),
					"responded":"false",
					"Response":" ",
					"twilioMessageSid": twiliowResp[1],
					"metaDataJSON":request
				}	
				print database.insertObj(logRequest, "requests")
				return {"Sucsess":"message sent Keep an eye on your phone for a responses", "toUser":toUser}
			else:
				return {"error":str(twiliowResp[0])}
		else:
			return {"error":"please wait till teacher responds or ticket expires "+ str(waitTime)}
		#print database.insertObj(logRequest, "requests")
		
		
	def MessageResponse(model, request):
		number = request["From"][0].split('+')[1]
		usercheck = database.get_row("SELECT * FROM users where telephone='{}' LIMIT 1".format(number))
		que = request["Body"][0].split(' ', 1)
		check = database.get_row("SELECT * FROM requests where toUserId='{}' and people='{}' and Status='Active' LIMIT 1".format(usercheck['userId'], str(que[0])))
		check1 = database.get_results("SELECT * FROM requests where toUserId='{}' and people='{}' and Status='Active' LIMIT 1".format(usercheck['userId'], str(que[0])))
		print usercheck['userId']
		print str(que[0])
		if not check1:
			print "error"
		else:
			try:
				if check['responded'] == "false":
					pulluser = database.get_row("SELECT * FROM users where userId='{}' LIMIT 1".format(check['fromUserId']))
					response = twiliow.Notify(str(pulluser['telephone']), usercheck['name'], que[1])
					database.executeSQL("UPDATE requests SET Status='Closed', responded='true', response='{}' where requestId='{}'".format(str(que[1]),check['requestId']))
					return {"sucsess":response}
				else:
					print "Error	"
			except ValueError as e:
				print e
