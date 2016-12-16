import database

class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM users where name='{}' LIMIT 1".format(name)
		data = database.get_results(query)
		
		if("error" in data[0]): 
			return { "error" : data[0]["error"]}
		
		if len(data) == 0: 
			return { "error" : "Person not found."}

		return data[0]


	def addPerson(model, request):
		person = request["person"]
		return database.insertObj(person, "users")
