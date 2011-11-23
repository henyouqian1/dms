from struct import *
from cStringIO import StringIO
from flask import *
import MySQLdb
#import json
import sys

import dmsDev
import dmsUser

import dmsDevView
import dmsUserView

# create our little application :)
app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(dmsDev.devBluePrint)
app.register_blueprint(dmsUser.userBluePrint)


def connect_db():
    return MySQLdb.connect(host="localhost",user="root",
                  		passwd="verygame123",db="dms",charset = "utf8")

@app.before_request
def before_request():
	g.conn=connect_db()
	g.cur=g.conn.cursor()
	g.urltimeout=200

@app.teardown_request
def teardown_request(exception):
	g.cur.close()
	g.conn.close()
	
import time
@app.route('/ltask')
def ltask():
	time.sleep(50)
	return "long finish"

import random
@app.route('/stask')
def stask():
	i = random.randint(0, 1000)
	print i
	return "s finish %i" % i


from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
	#http_server = HTTPServer(WSGIContainer(app))
	#http_server.bind(8000)
	#http_server.start(0)
	#IOLoop.instance().start()