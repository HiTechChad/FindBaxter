

#import system libs
import mysql.connector, os, json, sys
from gevent.pywsgi import WSGIServer
from gevent import monkey
from cgi import parse_qs, escape
monkey.patch_all() # makes many blocking calls asynchronous


# import application objects
sys.path.insert(0, '../../config') # moved outside repo to be system-specific
import config, website, database, model


def application(environ, start_response):

	# if we're requesting a page or a file, get it
	if environ["REQUEST_METHOD"] == "GET": 
		return website.return_static(environ, start_response)



	# handle POST api requests
	if environ["REQUEST_METHOD"] == "POST": 

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

			# IS THERE A RESPONSE?
			response = r

		else :

			# get input
			try:
				r = json.loads(environ["wsgi.input"].read())
			except ValueError as e:
				print e
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





	


