import database
import config

class AppModel:

	def getPerson(model, request):
		name = request["name"]
		query = "SELECT * FROM users where name='{}' LIMIT 10".format(name)
		data = database.get_results(query)
		if len(data) == 0: return { "error_message" : "Person not found."}
		return data[0]
	def addPerson():
		c = config.conn
		c.ping(True)
		cur = c.cursor()
		add_user = ("INSERT INTO users "
              "(userId, name, pic, email) "
              "VALUES (%(userId)s, %(name)s, %(pic)s, %(email)s)")
		emp_no = cursor.lastrowid
		data_user = {
		  'userId': emp_no,
		  'name': "CHARDDDD IS",
		  'pic': "",
		  'email': "DBOMB@GMAIL",
		}
		cur.execute(add_user, data_user)
		c.commit();