

#import system libs
import mysql.connector, os, json, model
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all() # makes many blocking calls asynchronous


# import application objects
import config, website, database, model


def application(environ, start_response):

	# if we're requesting a page or a file, get it
	if environ["REQUEST_METHOD"] == "GET": 
		return website.return_static(environ, start_response)



	# handle POST api requests
	if environ["REQUEST_METHOD"] == "POST": 

		# get input
		r = json.loads(environ["wsgi.input"].read())
		if "verb" in r : 
			v = r["verb"]
			m = model.AppModel()
			if v in dir(m): 
			 	response = getattr(m, v)(r) #do this shit!
			else:
				response = { "error_message" : "That action is unavailable."}
		else:
			response = { "error_message" : "No action requested."}


		
		# send response
		headers = [
			('content-type', 'application/json'),
    		("Access-Control-Allow-Origin", "*")
		]
		start_response('200 OK', headers)
		return [json.dumps(response)]




address = "localhost", 8888
server = WSGIServer(address, application)
server.backlog = 256
server.serve_forever()





	


