

#import system libs
import mysql.connector, os, json, sys, twiliow, requests, random, string
from gevent.pywsgi import WSGIServer
from gevent import monkey
from cgi import parse_qs, escape
monkey.patch_all() # makes many blocking calls asynchronous


# import application objects
sys.path.insert(0, '../../config') # moved outside repo to be system-specific
import config, website, database, model, guid
from oauth2client import client, crypt

def runRequest(environ):
	# get input
	httpReq = environ["wsgi.input"].read()
	try:
		r = json.loads(httpReq, strict=False)
		
	except ValueError as e:
		return { "error" : "Bad JSON! Bad!"}

	if "verb" in r : 
		v = r["verb"]

		if v == "login":
			return loginUser(r)

		r["user"] = parseAccessToken(r)
		if "error" in r["user"]:
			return r["user"]

		m = model.AppModel()
		
		if v in dir(m): 
		 	return getattr(m, v)(r) #do this shit!
		else:
			return { "error" : "That action is unavailable."}
	else:
		return { "error" : "No action requested."}


def parseAccessToken(r):

	 if "access_token" in r:

	 	# look up user in users table where access_token = r["access_token"]
		user = database.get_results("SELECT * FROM users WHERE guid='{}' LIMIT 1".format(r["access_token"]))
	 	# if user found
		if user:
	 		# check expiration date of session
			return user
			 	# if good, return user

			 	# if not, return { "error" : "Session Expired" }

	 	# else return { "error" : "Bad Token" }
		else:
			return {"error": "Bad Token"}
	 else :
	 	# return { "error" : "No Access Token" }
		return {"error": "No Access Token"}


def loginUser(r):

	 if "google_token" in r:
			
	 	# look up google_token using HTTP API
		try:
			Authentication = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + r['google_token']).json()
		except(TypeError):
			return {"error":"failed to check google"}
	 	# if user found in Google, look for user in users table
		if "error_description" not in Authentication:
			user = database.get_results("SELECT * FROM users where name='{}' LIMIT 1".format(Authentication['name']))
	 		# if user found in table 
			if not user:
				# generate new user with info from Google
				guid = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
				newUser = {
					"name":Authentication['name'],
					"pic":Authentication['picture'],
					"email":Authentication['email'],
					"guid":guid
				}
	 			# insert into users table
				database.insertObj(newUser, "users")
	 			# return { "access_token" : "new access_token" }
				return {"response":guid, "user": user}
			if user:
				user = database.get_row("SELECT * FROM users where name='{}' LIMIT 1".format(Authentication['name']))
				# generate new access_token
				guid = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
	 			# update users table
				database.executeSQL("UPDATE users SET guid='{}' WHERE name='{}'".format(str(guid), user['name']), True)
	 			# return { "access_token" : "new access_token" }
				return {"response":guid, "user": user}
				# if user not found in table
		else:
			return {"error": "Bad Google Token"}
	 else :
	 	return { "error" : "No Google Token" }



def application(environ, start_response):

	# if we're requesting a page or a file, get it
	if environ["REQUEST_METHOD"] == "GET": 
		return website.return_static(environ, start_response)



	# handle POST api requests
	if environ["REQUEST_METHOD"] == "POST":

		# if it's twilio
		if environ['PATH_INFO'] == "/twilio_callback" :
		# READ TWILIO RESPONSE INTO REQUEST OBJECT r
			try:
				request_body_size = int(environ.get('CONTENT_LENGTH', 0))
			except (ValueError):
				request_body_size = 0

			request_body = environ['wsgi.input'].read(request_body_size)
			r = parse_qs(request_body)


			# DO SOMETHING WITH r
			# ...
			if r["AccountSid"][0] == "ACd37c9f284658c4b14ed1878a1b4f7feb": 
				m = model.AppModel()
				v = "MessageResponse"
				if v in dir(m): 
					response = getattr(m, v)(r) #do this shit!
				else:
					response = { "error" : "That action is unavailable."}
					
		# EVERYTHING else
		else :
			response = runRequest(environ)


		
		# send response
		headers = [
			('content-type', 'application/json'),
    		("Access-Control-Allow-Origin", "*")
		]
		start_response('200 OK', headers)
		return [json.dumps(response, indent=5)]




address = "localhost", 8888
server = WSGIServer(address, application)
server.backlog = 256
server.serve_forever()





	


