# Python and Gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all() # makes many blocking calls asynchronous

def application(environ, start_response):
    if environ["REQUEST_METHOD"]!="POST": # your JS uses post, so if it isn't post, it isn't you
        start_response("403 Forbidden", [("Content-Type", "text/html; charset=utf-8")])
        return "403 Forbidden"
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    r = environ["wsgi.input"].read() # get the post data
    return r

address = "localhost", 8080
server = WSGIServer(address, application)
server.backlog = 256
server.serve_forever()
