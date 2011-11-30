from flask import *
import MySQLdb
from dmsConfig import *
import hashlib
import uuid
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
	email = request.args.get('email', type=unicode)
	password = request.args.get('password', type=unicode)
	if ( email==None or password==None ):
		return jsonify(error='pram error')
	g.cur.execute('SELECT password, developer_id FROM Developers WHERE email=%s', email)
	row = g.cur.fetchone()
	if ( row == None ):
		return jsonify(error='Email not exist.')
	else:
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
	email = request.args.get('email', type=unicode)
	password = request.args.get('password', type=unicode)
	if ( email==None or password==None ):
		return jsonify(error='pram error')
	#todo: check email and password
	shapw = hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
	secretkey = uuid.uuid4().hex;
	try:
		g.cur.execute('INSERT INTO Developers (email, password, secret_key) VALUES(%s, %s, %s)', (email, shapw, secretkey))
		g.conn.commit()
	except:
		return jsonify(error='email already exist.')
	
	session['developer_email'] = email
	g.cur.execute('SELECT developer_id FROM Developers WHERE email=%s', email)
	row = g.cur.fetchone()
	session['developer_id'] = row[0]
	
	return jsonify(error=0, developerid=session['developer_id'], developeremail=session['developer_email'])

@devBluePrint.route('/dms/devgetsecretkey')
def devgetsecretkey():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	g.cur.execute('SELECT secret_key FROM Developers WHERE developer_id=%s', session['developer_id'])
	row = g.cur.fetchone()
	return jsonify(secretkey=row[0]);

###award
@devBluePrint.route('/dms/devgetawards')
def devgetawards():
	if ('developer_id' in session):
		page = request.args.get('page', type=int)
		num = request.args.get('num', type=int)
		if ( page==None or num==None ):
			return jsonify(error='pram error')
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
	name = request.args.get('name', type=unicode)
	desc = request.args.get('desc', type=unicode)
	img = request.args.get('img', type=unicode)
	if ( name==None or desc==None or img==None ):
		return jsonify(error='pram error')
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
	awardId = request.args.get('id', type=int)
	name = request.args.get('name', type=unicode)
	desc = request.args.get('desc', type=unicode)
	img = request.args.get('img', type=unicode)
	if ( awardId==None or name==None or desc==None or img==None ):
		return jsonify(error='pram error')
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
	awardId = request.args.get('id', type=int)
	if ( awardId==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('DELETE FROM Awards WHERE developer_id=%s AND award_id=%s', (session['developer_id'], awardId))
		g.conn.commit()
	except:
		return jsonify(error='delete award failed.')
	return jsonify(error=0)

###game
@devBluePrint.route('/dms/devgetgames')
def devgetgames():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	try:
		g.cur.execute('SELECT game_id, name, score_lower_better FROM Games WHERE developer_id=%s', (session['developer_id'],))
		data = [{'id':row[0], 'name':row[1], 'lowerbetter':row[2]} for row in g.cur.fetchall()]
		return jsonify(error=0, data=data)
	except Exception, e:
		print e
		return jsonify(error='sql error.')
		
@devBluePrint.route('/dms/devaddgame')
def devaddgame():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	name = request.args.get('name', type=unicode)
	lowerbetter = request.args.get('lowerbetter', type=int)
	if ( name==None or lowerbetter==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('INSERT INTO Games (developer_id, name, score_lower_better) VALUES(%s, %s, %s)', (session['developer_id'], name, lowerbetter))
		g.conn.commit()
	except MySQLdb.IntegrityError as e:
		if ( e.args[0] == 1062 ):
			return jsonify(error='game "%s" already exists'%name)
		else:
			return jsonify(error='add game failed')
	except Exception:
		return jsonify(error='add game failed')
	return jsonify(error=0)

@devBluePrint.route('/dms/deveditgame')
def deveditgame():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	gameId = request.args.get('id', type=int)
	name = request.args.get('name', type=unicode)
	lowerbetter = request.args.get('lowerbetter', type=int)
	if ( gameId==None or name==None or lowerbetter==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('UPDATE Games SET name=%s, score_lower_better=%s WHERE developer_id=%s AND game_id=%s', (name, lowerbetter, session['developer_id'], gameId))
		g.conn.commit()
	except MySQLdb.IntegrityError as e:
		if ( e.args[0] == 1062 ):
			return jsonify(error='game "%s" already exists'%name)
		else:
			return jsonify(error='edit game failed')
	except Exception:
		return jsonify(error='edit game failed')
	return jsonify(error=0)


@devBluePrint.route('/dms/devdeletegame')
def devdeletegame():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	gameid = request.args.get('id', type=int)
	if ( gameid==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('DELETE FROM Games WHERE developer_id=%s AND game_id=%s', (session['developer_id'], gameid))
		g.conn.commit()
	except:
		return jsonify(error='delete game failed.')
	return jsonify(error=0)
	
###match
@devBluePrint.route('/dms/devgetmatches')
def devgetmatches():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	page = request.args.get('page', type=int)
	num = request.args.get('num', type=int)
	if ( page==None or num==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('SELECT m.match_id, m.name, m.date, m.game_id, g.name FROM Matches AS m INNER JOIN Games AS g ON m.game_id=g.game_id WHERE m.developer_id=%s ORDER BY m.date DESC LIMIT %s OFFSET %s', (session['developer_id'],num, page*num))
		data = [{'id':row[0], 'name':row[1], 'date':str(row[2]), 'gameid':row[3], 'gamename':row[4]} for row in g.cur.fetchall()]
		return jsonify(error=0, data=data)
	except Exception, e:
		return jsonify(error=str(e))
		
@devBluePrint.route('/dms/devaddmatch')
def devaddmatch():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	name = request.args.get('name', type=unicode)
	date = request.args.get('date', type=unicode)
	gameid = request.args.get('gameid', type=int)
	if ( name==None or date==None or gameid==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('INSERT INTO Matches (developer_id, name, date, game_id) VALUES(%s, %s, %s, %s)', (session['developer_id'], name, date, gameid))
		g.conn.commit()
	except Exception:
		return jsonify(error='add game failed')
	return jsonify(error=0)
	
@devBluePrint.route('/dms/deveditmatch')
def deveditmatch():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	matchid = request.args.get('matchid', type=int)
	name = request.args.get('name', type=unicode)
	date = request.args.get('date', type=unicode)
	gameid = request.args.get('gameid', type=int)
	if ( matchid==None or name==None or date==None or gameid==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('UPDATE Matches SET name=%s, date=%s, game_id=%s WHERE developer_id=%s AND match_id=%s', (name, date, gameid, session['developer_id'], matchid))
		g.conn.commit()
	except Exception:
		return jsonify(error='edit game failed')
	return jsonify(error=0)
	
@devBluePrint.route('/dms/devdeletematch')
def devdeletematch():
	if ('developer_id' not in session):
		return jsonify(error='need login.')
	matchid = request.args.get('matchid', type=int)
	if ( matchid==None ):
		return jsonify(error='pram error')
	try:
		g.cur.execute('DELETE FROM Matches WHERE developer_id=%s AND match_id=%s', (session['developer_id'], matchid))
		g.conn.commit()
	except:
		return jsonify(error='delete game failed.')
	return jsonify(error=0)