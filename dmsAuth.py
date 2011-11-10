from flask import *
import urllib2
import urlparse
import MySQLdb
from dmsConfig import *
import hashlib

authBluePrint = Blueprint('auth', __name__)

@authBluePrint.route('/dms/trylogin')
def tryLogin():
	if ( 'user_id' in session ):
		return jsonify(login=1)
	else:
		return jsonify(login=0)

@authBluePrint.route('/dms/login')
def login():
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
			session['email'] = email
			return jsonify(error=0)
		else:
			return jsonify(error='Wrong password.')
	
@authBluePrint.route('/dms/logout')
def logout():
	rootURL=url_for('dmsRoot', _external=True)
	if ( 'fbUserId' in session ):
		session.clear()
		url='https://www.facebook.com/logout.php?next=%s&access_token=%s' % (rootURL, session['fbSessionToken'])
		return jsonify(url=url)
	session.clear()
	return jsonify(url=rootURL)

@authBluePrint.route('/dms/fblogin')
def fblogin():
	code = request.args.get('code', '', type=unicode)
	url="https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (APPID, url_for('.fblogin', _external=True), APPSECRET, code)
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
	
	g.cur.execute('SELECT user_id FROM Users WHERE facebook_id=%s', id)
	row = g.cur.fetchone()
	if (row == None):
		return render_template('dmsRegister.html')
	else:
		session['user_id']=row[0]
	return render_template('dmsConsole.html', fbUserId=session['fb_user_id'])
	
@authBluePrint.route('/dms/register')
def register():
	email = request.args.get('email', '', type=unicode)
	password = request.args.get('password', '', type=unicode)
	#todo: check email and password
	print hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
	shapw = hashlib.sha256(password+PASSWORDAPPEND).hexdigest()
	if ( 'fbUserId' in session ):
		g.cur.execute('UPDATE Users SET email=%s, password=%s WHERE facebook_id=%s', (email, shapw, session['fbUserId']))
		g.conn.commit()
	else:
		try:
			g.cur.execute('INSERT INTO Users (email, password) VALUES(%s, %s)', (email, shapw))
			g.conn.commit()
		except:
			return jsonify(error='email already exist.')
		session['email'] = email
		g.cur.execute('SELECT user_id FROM Users WHERE email=%s', email)
		row = g.cur.fetchone()
		session['user_id'] = row[0]
	return jsonify(error=0)