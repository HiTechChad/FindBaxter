
import config, mysql.connector

def executeSQL(query):
	c = config.conn
	c.ping(True)
	cur = c.cursor()

	try:
		cur.execute(query)
		return {"cursor" : cur }

	except mysql.connector.Error as e:
		cur.close()
		return {"error" : "MySQL Error: %s" % str(e)}


#RUN QUERY AND GET ROW
def get_row(query) :

	# Run Query
	dbResponse = executeSQL(query)
	if("error" in dbResponse) : return dbResponse

	# Build Response Object
	cur = dbResponse["cursor"]
	columns = tuple( [d[0].decode('utf8') for d in cur.description] ) 
	for row in cur: 
		response = dict(zip(columns, row))
		cur.close() 
		return response

	return {"error" : "Object Not Found"}



# RUN QUERY AND RETURN DATA OBJECT
def get_results(query) :

	# Run Query
	dbResponse = executeSQL(query)
	if("error" in dbResponse) : dbResponse

	# Build Response Object
	cur = dbResponse["cursor"]
	columns = tuple( [d[0].decode('utf8') for d in cur.description] ) 
	result = [] 
	for row in cur: result.append(dict(zip(columns, row))) 
	cur.close() 
	return result


# ADD OBJ TO TABLE
def insertObj(obj, tableName):

	d = dict(obj)  

	# Write SQL Query
	query = "INSERT INTO {0} ({1}) VALUES ({2})"
	columns = ','.join(d.keys())
	placeholders = ','.join(['"%s"'] * len(d))
	sql = query.format(tableName, columns, placeholders) % tuple(d.values())

	# Run It and Handle Error
	dbResponse = executeSQL(sql)

	if ("error" in dbResponse) : return dbResponse

	else :
		cursor = dbResponse["cursor"]
		response = ("newId", cursor.lastrowid)
		cursor.close() 
		config.conn.commit()
		return response



