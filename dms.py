from struct import *
from cStringIO import StringIO
from flask import *
import MySQLdb
#import json
import sys

import dmsAuth
import dmsMain
import dmsDev

import dmsAuthView
import dmsMainView
import dmsDevView

# create our little application :)
app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(dmsAuth.authBluePrint)
app.register_blueprint(dmsMain.mainBluePrint)
app.register_blueprint(dmsDev.devBluePrint)


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
	
@app.route('/dms')
def dmsRoot():
	return render_template('dmsRoot.html')
	
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    return jsonify(result=a + b)

@app.route('/')
def index():
	code = request.args.get('code', '', type=unicode)
	return render_template('test.html')

@app.route('/dms/xxx')
def dmsxxx():
	return render_template('dms.html')

@app.route('/lsGames')
def lsGames():
	g.cur.execute('SELECT game_id, name, score_small_better, modify_datetime FROM Games ORDER BY game_id ASC')
	th = ['game_id', 'name', 'score_small_better', 'modify_datetime']
	trs = [[row[0], row[1], row[2], str(row[3])] for row in g.cur.fetchall()]
	return jsonify(th=th, trs=trs)
	
@app.route('/addGame')
def addGame():
	name = request.args.get('name', type=unicode)
	scoreSmallBetter = request.args.get('scoreSmallBetter', 0, type=int)
	g.cur.execute('INSERT INTO Games (name, score_small_better, modify_datetime) VALUES(%s, %s, NOW())', (name,scoreSmallBetter))
	#todo check succeed
	g.conn.commit()
	return jsonify(result=1)
	
@app.route('/editGame')
def editGame():
	id = request.args.get('id', -1, type=int)
	name = request.args.get('name', '', type=unicode)
	scoreSmallBetter = request.args.get('scoreSmallBetter', type=int)
	g.cur.execute('UPDATE Games SET name=%s, score_small_better=%s, modify_datetime=NOW() WHERE game_id=%s', (name,scoreSmallBetter,id))
	#todo check succeed
	g.conn.commit()
	return jsonify(result=1)
	
@app.route('/delGame')
def delGame():
	id = request.args.get('id', -1, type=int)
	g.cur.execute('DELETE FROM Games WHERE game_id=%s', (id,))
	#todo check succeed
	g.conn.commit()
	return jsonify(result=1)
	
@app.route('/lsTournaments')
def lsTournaments():
	g.cur.execute('SELECT tournament_id, title, match_num, begin_date, end_date, is_publish, modify_datetime FROM Tournaments ORDER BY tournament_id ASC')
	th = ['tournament_id', 'title', 'match_num', 'begin_date', 'end_date', 'is_publish', 'modify_datetime']
	trs = [[row[0], row[1], row[2], str(row[3]), str(row[4]), row[5], str(row[6])] for row in g.cur.fetchall()]
	return jsonify(th=th, trs=trs)
	
@app.route('/lsMatchs')
def lsMatchs():
	th = ['match_id', 'tournament_id', 'game_id', 'date', 'prev_match_id', 'pass_mode']
	trs = []
	return jsonify(th=th, trs=trs)
	
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