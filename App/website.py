import os, json

def return_static(environ, start_response):

	path = environ['PATH_INFO']
	if(path == '' or path == '/') : path = '/index.html'
	
	path = os.getcwd() + "/client" + path

	# if path exists
	if os.path.exists(path):

		# get the content
		h = open(path, 'rb')
		content = h.read()
		h.close()


		# set the mime type
		MIME_TABLE = {
			'.txt': 'text/plain',
			'.html': 'text/html',
			'.css': 'text/css',
			'.js': 'application/javascript',
		}
		name, ext = os.path.splitext(path)
		contentType = MIME_TABLE[ext] if ext in MIME_TABLE else "application/octet-stream"  	
    
		
		# return static asset
		headers = [
			('content-type', contentType),
    		("Access-Control-Allow-Origin", "*")
    	]
		start_response('200 OK', headers)
		return [content]


	# if not, handle the missing file
	else:
		headers = [('content-type', 'text/html')]
		start_response('404', headers)
		return ["Bad Path"]




