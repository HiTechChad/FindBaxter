import database

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
		query = "SELECT * FROM users"
		return database.get_results(query)
		
		