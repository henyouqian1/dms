from flask import *
import urllib2
import urlparse
import MySQLdb
from dmsConfig import *
import hashlib

userBluePrint = Blueprint('user', __name__)

@userBluePrint.route('/dms/userislogin')
def userislogin():
	if ( ('user_id' in session) and ('user_email' in session) ):
		return jsonify(login=1, userid=session['user_id'], useremail=session['user_email'])
	else:
		session.clear()
		return jsonify(login=0)

@userBluePrint.route('/dms/userlogin')
def userlogin():
	session.clear()
	email = request.args.get('email', '', type=unicode)
	password = request.args.get('password', '', type=unicode)
	g.cur.execute('SELECT password, user_id FROM Users WHERE email=%s', email)
	row = g.cur.fetchone()
	if ( row == None ):
		return jsonify(error='Email not exist.')
	else:
		print row[0]
		print hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
		if ( row[0] == hashlib.sha256(password+PASSWORDAPPEND).hexdigest() ):
			session['user_id'] = row[1]
			session['user_email'] = email
			return jsonify(error=0, userid=session['user_id'], useremail=session['user_email'])
		else:
			return jsonify(error='Wrong password.')
			
@userBluePrint.route('/dms/userlogout')
def userlogout():
	session.clear()
	return jsonify(error=0)
	
@userBluePrint.route('/dms/userregister')
def userregister():
	email = request.args.get('email', '', type=unicode)
	password = request.args.get('password', '', type=unicode)
	#todo: check email and password
	print hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
	shapw = hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
	try:
		g.cur.execute('INSERT INTO Users (email, password) VALUES(%s, %s)', (email, shapw))
		g.conn.commit()
	except:
		return jsonify(error='email already exist.')
	session['user_email'] = email
	g.cur.execute('SELECT user_id FROM Users WHERE email=%s', email)
	row = g.cur.fetchone()
	session['user_id'] = row[0]
	return jsonify(error=0, userid=session['user_id'], useremail=session['user_email'])
	
@userBluePrint.route('/dms/userfblogin')
def userfblogin():
	code = request.args.get('code', '', type=unicode)
	url="https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (APPID, url_for('.userfblogin', _external=True), APPSECRET, code)
	#&type=client_cred
	f=urllib2.urlopen(url);
	s=f.read()
	o=urlparse.parse_qs(s)
	token=o['access_token'][0]
	graph_url = "https://graph.facebook.com/me?access_token=%s"%token
	f=urllib2.urlopen(graph_url);
	s=f.read()
	jdata=json.loads(s)
	id=jdata['id']
	session['fb_user_id']=id
	session['fb_token']=token
	
	g.cur.execute('SELECT user_id, email FROM Users WHERE facebook_id=%s', id)
	row = g.cur.fetchone()
	if (row != None):
		session['user_id']=row[0]
		session['email_id']=row[1]
	else:
		session.pop('user_id', None)
		session.pop('email_id', None)
	return redirect(url_for('.userview', _external=True))