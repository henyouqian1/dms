from struct import *
from cStringIO import StringIO
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import MySQLdb
from lwMsg import *

# create our little application :)
app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return MySQLdb.connect(host="localhost",user="root",
                  		passwd="verygame123",db="dms",charset = "utf8")

@app.before_request
def before_request():
	g.db=connect_db()
	g.cur=g.db.cursor()

@app.teardown_request
def teardown_request(exception):
	g.cur.close()
	g.db.close()

@app.route('/lwAdd', methods=['POST'])
def lwAdd():
	input = StringIO(request.data)
	v1 = readFloat(input)
	v2 = readFloat(input)
	str = readUtf8(input)
	output = StringIO()
	writeFloat(output, v1+v2)
	writeUtf8(output, str)
	return output.getvalue()
	
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('test.html')
    
@app.route('/dms')
def dms():
    return render_template('dms.html')
    
@app.route('/lsGames')
def lsGames():
	g.cur.execute('SELECT game_id, name, big_is_better, modify_datetime FROM Games ORDER BY game_id ASC')
	th = ['game_id', 'name', 'big_is_better', 'modify_datetime']
	trs = [[row[0], row[1], row[2], str(row[3])] for row in g.cur.fetchall()]
	return jsonify(th=th, trs=trs)
	
@app.route('/addGame')
def addGame():
	name = request.args.get('name', '', type=str)
	bigIsBetter = request.args.get('bigIsBetter', 1, type=int)
	g.cur.execute('INSERT INTO Games (name, big_is_better, modify_datetime) VALUES(%s, %s, NOW())', (name,bigIsBetter))
	#todo check succeed
	g.db.commit()
	return jsonify(result=1)
	
@app.route('/editGame')
def editGame():
	id = request.args.get('id', -1, type=int)
	name = request.args.get('name', '', type=str)
	bigIsBetter = request.args.get('bigIsBetter', 1, type=int)
	g.cur.execute('UPDATE Games SET name=%s, big_is_better=1, modify_datetime=NOW() WHERE game_id=%s', (name,id))
	#todo check succeed
	g.db.commit()
	return jsonify(result=1)
	
@app.route('/delGame')
def delGame():
	id = request.args.get('id', -1, type=int)
	g.cur.execute('DELETE FROM Games WHERE game_id=%s', (id,))
	#todo check succeed
	g.db.commit()
	return jsonify(result=1)

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
    #http_server = HTTPServer(WSGIContainer(app))
    #http_server.listen(8000)
    #IOLoop.instance().start()
