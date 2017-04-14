

#import system libs
import mysql.connector, os, json, sys, twiliow, requests
from gevent.pywsgi import WSGIServer
from gevent import monkey
from cgi import parse_qs, escape
monkey.patch_all() # makes many blocking calls asynchronous


# import application objects
sys.path.insert(0, '../../config') # moved outside repo to be system-specific
import config, website, database, model, guid
from oauth2client import client, crypt

def application(environ, start_response):

	# if we're requesting a page or a file, get it
	if environ["REQUEST_METHOD"] == "GET": 
		return website.return_static(environ, start_response)



	# handle POST api requests
	if environ["REQUEST_METHOD"] == "POST": 
	
		if environ['PATH_INFO'] == "/oAuth":
			httpReq = environ["wsgi.input"].read()
			try:
				r = json.loads(httpReq, strict=False)
				
			except ValueError as e:
				response = { "error" : "Bad JSON! Bad!"}
				r = {}	
			if "initToken" in r:
				v = r['initToken']
				Authentication = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + v).json()
				if "error_description" not in Authentication	:
					searchUserTable = database.get_results("SELECT * FROM users where email='{}' LIMIT 1".format(check['email']))
					if not searchUserTable:
						addNewUser = {
							"name":Authentication['name'],
							"pic":Authentication['picture'],
							"email":Authentication['email'],
							"guid":guid.id_generator()
						}
						database.insertObj(addNewUser, "users")
						return {"Sucsess":"User Authenticated Sucsessfully, Added New User"}
					else:
						return searchUserTable['guid']
				else:
					{"Error": "INVALID AUTHENTICATION YOU SHALL NOT PASS"}
			
			
			
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

				
			

			
			# IS THERE A RESPONSE?
			

		else :

			# get input
			httpReq = environ["wsgi.input"].read()
			try:
				r = json.loads(httpReq, strict=False)
				
			except ValueError as e:
				response = { "error" : "Bad JSON! Bad!"}
				r = {}	
			if "accsess_token" in r:
				Authentication = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + r["accsess_token"]).json()
			if "verb" in r : 
				v = r["verb"]
				m = model.AppModel()
				
				if v in dir(m): 
				 	response = getattr(m, v)(r) #do this shit!
				else:
					response = { "error" : "That action is unavailable."}
			else:
				response = { "error" : "No action requested."}


		
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





	


