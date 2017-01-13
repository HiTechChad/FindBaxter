import database, twiliow, json, recieve

class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM users where name='{}' LIMIT 1".format(name)
		return database.get_row(query)
		

	def addPerson(model, request):
		person = request["person"]
		return database.insertObj(person, "users")

		
	'''
	getPeople
	- @param:
		// if no param, return all people
		
	- @return PEOPLE LIST
		[
			{ person (see above)},
			{ person (see above)}
	]
	'''
	def getPeople(model, request):
		query = "SELECT name, pic, email FROM users"
		return database.get_results(query)
		
	def sendTxt(model, request):
		username = ['username']
		authToken = ['authToken']
		name = request["name"]
		meeting = request["type"]
		checkUser = "SELECT * FROM users where name='{}' LIMIT 1".format(username)
		if(checkUser['auth'] = authToken):
			database.get_row(checkUser)
			query = "SELECT telephone FROM users where name='{}' LIMIT 1".format(name)
			twiliow.MessageUser(database.get_results(query)['telephone'], type)
		else:
			return {"error":"failed to authenticate"}
	def UpdateAuth(modle, request):
		name = request["name"]
		authToken = ['authToken']
		query = "SELECT * FROM users where name='{}' LIMIT 1".format(name)
		if(database.get_row(query) != {"error" : "Object Not Found"}):
			return database.insertObj(person, "users")

		