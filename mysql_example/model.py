import database

class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM users where name='{}' LIMIT 1".format(name)
		return database.get_row(query)
		

	def addPerson(model, request):
		if (!("person" in request)) :
			return {"error" : "Request Error: No person requested"}
		person = request["person"]
		return database.insertObj(person, "users")
