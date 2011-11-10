from flask import *
import MySQLdb
from dmsConfig import *
import hashlib

devBluePrint = Blueprint('dev', __name__)
	
@devBluePrint.route('/dms/devlogin')
def devlogin():
	session.clear()
	email = request.args.get('email', '', type=unicode)
	password = request.args.get('password', '', type=unicode)
	g.cur.execute('SELECT password, developer_id FROM Developers WHERE email=%s', email)
	row = g.cur.fetchone()
	if ( row == None ):
		return jsonify(error='Email not exist.')
	else:
		print row[0]
		print hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
		if ( row[0] == hashlib.sha256(password+PASSWORDAPPEND).hexdigest() ):
			session['developer_id'] = row[1]
			session['developer_email'] = email
			return jsonify(error=0)
		else:
			return jsonify(error='Wrong password.')
	
@devBluePrint.route('/dms/devlogout')
def devlogout():
	loginURL=url_for('.devloginview', _external=True)
	session.clear()
	return jsonify(url=loginURL)
	
@devBluePrint.route('/dms/devregister')
def devregister():
	email = request.args.get('email', '', type=unicode)
	password = request.args.get('password', '', type=unicode)
	#todo: check email and password
	shapw = hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
	try:
		g.cur.execute('INSERT INTO Developers (email, password) VALUES(%s, %s)', (email, shapw))
		g.conn.commit()
	except:
		return jsonify(error='email already exist.')
	
	session['developer_email'] = email
	g.cur.execute('SELECT developer_id FROM Developers WHERE email=%s', email)
	row = g.cur.fetchone()
	session['developer_id'] = row[0]
	
	return jsonify(error=0)
	
	

