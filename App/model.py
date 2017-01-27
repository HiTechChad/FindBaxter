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
	def test(model, request):
		fromUser = request['username']
		toUser = request["name"]
		fromQuery = "SELECT * FROM users where name='{}' LIMIT 1".format(fromUser)
		toQuery = "SELECT * FROM users where name='{}' LIMIT 1".format(toUser)
		logRequest = json.loads({
			"from":str(fromUser),
			"too_number":str(database.get_row(toQuery)['telephone']),
			"too":str(toUser),
			"from_number":str(database.get_row(fromQuery)['telephone']),
			"time":str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')),
			"responded":"false"
		})
		print logRequest
		print database.insertObj(logRequest, "requests")
'''	def sendTxt(model, request):
		fromUser = request['username']
		authToken = request['authToken']
		tooUser = request["name"]
		meeting = request["type"]
		fromQuery = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(fromUser))
		toQuery = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(tooUser))
		if(fromQuery['authToken'] == str(authToken)):
			if(twiliow.MessageUser(toQuery['telephone'], meeting, fromUser)):
		else:
			return {"error":"failed to authenticate"}
'''

'''	def Auth(modle, request):
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
'''
