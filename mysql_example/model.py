import database


class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM users where name='{}' LIMIT 10".format(name)
		data = database.get_results(query)
		if len(data) == 0: return { "error_message" : "Person not found."}
		return data[0]

