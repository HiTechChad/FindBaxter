
import config

def executeSQL(query):
	c = config.conn
	c.ping(True)
	cur = c.cursor()
	cur.execute(query)
	return cur


# RUN QUERY AND RETURN DATA OBJECT
def get_results(query) :
	cur = executeSQL(query)
	columns = tuple( [d[0].decode('utf8') for d in cur.description] ) 
	result = [] 
	for row in cur: result.append(dict(zip(columns, row))) 
	cur.close() 
	return result

