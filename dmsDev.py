from flask import *
import MySQLdb
from dmsConfig import *
import hashlib
import sys

devBluePrint = Blueprint('dev', __name__)

@devBluePrint.route('/dms/devislogin')
def devislogin():
	if ( ('developer_id' in session) and ('developer_email' in session) ):
		return jsonify(login=1, developerid=session['developer_id'], developeremail=session['developer_email'])
	else:
		session.clear()
		return jsonify(login=0)
	
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
			return jsonify(error=0, developerid=session['developer_id'], developeremail=session['developer_email'])
		else:
			return jsonify(error='Wrong password.')
	
@devBluePrint.route('/dms/devlogout')
def devlogout():
	session.clear()
	return jsonify(error=0)
	
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
	
	return jsonify(error=0, developerid=session['developer_id'], developeremail=session['developer_email'])
	
@devBluePrint.route('/dms/devgetawards')
def devgetawards():
	if ('developer_id' in session):
		page = request.args.get('page', 0, type=int)
		num = request.args.get('num', 0, type=int)
		try:
			g.cur.execute('SELECT award_id, name, description, image FROM Awards WHERE developer_id=%s LIMIT %s OFFSET %s', (session['developer_id'], num, page*num))
			data = [{'idx':row[0], 'name':row[1], 'desc':row[2], 'img':row[3]} for row in g.cur.fetchall()]
			return jsonify(error=0, data=data)
		except Exception, e:
			print e
			return jsonify(error='sql error.')
	else:
		return jsonify(error='need login.')
		
@devBluePrint.route('/dms/devaddaward')
def devaddaward():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	name = request.args.get('name', '', type=unicode)
	desc = request.args.get('desc', '', type=unicode)
	img = request.args.get('img', '', type=unicode)
	try:
		g.cur.execute('INSERT INTO Awards (developer_id, name, description, image) VALUES(%s, %s, %s, %s)', (session['developer_id'], name, desc, img))
		g.conn.commit()
	except:
		return jsonify(error='add award failed.')
	return jsonify(error=0)
	
@devBluePrint.route('/dms/deveditaward')
def deveditaward():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	awardId = request.args.get('id', '', type=int)
	name = request.args.get('name', '', type=unicode)
	desc = request.args.get('desc', '', type=unicode)
	img = request.args.get('img', '', type=unicode)
	try:
		g.cur.execute('UPDATE Awards SET name=%s, description=%s, image=%s WHERE developer_id=%s AND award_id=%s', (name, desc, img, session['developer_id'], awardId))
		g.conn.commit()
	except Exception, e:
		print e
		return jsonify(error='edit award failed.')
	return jsonify(error=0)

@devBluePrint.route('/dms/devdeleteaward')
def devdeleteaward():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	awardId = request.args.get('id', '', type=int)
	try:
		g.cur.execute('DELETE FROM Awards WHERE developer_id=%s AND award_id=%s', (session['developer_id'], awardId))
		g.conn.commit()
	except:
		return jsonify(error='delete award failed.')
	return jsonify(error=0)

