import database, twiliow, json, recieve

class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM teachers where name='{}' LIMIT 1".format(name)
		return database.get_row(query)
		

	def addPerson(model, request):
		person = request["person"]
		return database.insertObj(person, "teachers")

		
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
		query = "SELECT name, pic, email FROM teachers"
		return database.get_results(query)
		
	def sendTxt(model, request):
		name = request["name"]
		meeting = request["mtype"]
		query = "SELECT telephone FROM teachers where name='{}' LIMIT 1".format(name)
		number = database.get_results(query)
		telephone = number[0]['telephone']
		message = twiliow.MessageUser(telephone, meeting)
		response = {"":""}
		if(message):
			response = {"message": "Message Sent"}
		else:
			response = {"error": "Message Not Sent"}
		return response
		