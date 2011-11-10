from flask import *
import urllib2
import urlparse
import MySQLdb
import socket

authBluePrint = Blueprint('auth', __name__)
APPID='239733542752050'
APPSECRET='430028de846e5c25369ae5bf0c3dd474'
FBTOKEN='239733542752050|uuy_7VoCrd5r9w2mOD3mx_pZPUw'
TIMEOUT=5.0
socket.setdefaulttimeout(TIMEOUT)
	
@authBluePrint.route('/dms/friends')
def friends():
	code = request.args.get('code', '', type=unicode)
	url="https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (APPID, url_for('.fbauth', _external=True), APPSECRET, code)
	#&type=client_cred
	f=urllib2.urlopen(url, timeout=TIMEOUT);
	s=f.read()
	o=urlparse.parse_qs(s)
	token=o['access_token'][0]
	graph_url = "https://graph.facebook.com/me/friends?access_token=%s"%token
	f=urllib2.urlopen(graph_url, timeout=TIMEOUT);
	s=f.read()
	jdata=json.loads(s)
	data=jdata['data']
	return s
	
@authBluePrint.route('/dms/login1')
def login():
	if ( 'fbUserId' in session ):
		return render_template('main.html', fbUserId=session['fbUserId'])
	else:
		return render_template('login.html')

@authBluePrint.route('/dms/logout')
def logout():
	if ( 'fbUserId' in session ):
		url='https://www.facebook.com/logout.php?next=%s&access_token=%s' % (url_for('.login', _external=True), session['fbSessionToken'])
		session.pop('fbUserId', None)
		return redirect(url)
	return render_template('login.html')
	
@authBluePrint.route('/dms/fbauth')
def fbauth():
	print 'fbauth'
	code = request.args.get('code', '', type=unicode)
	url="https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (APPID, url_for('.fbauth', _external=True), APPSECRET, code)
	#&type=client_cred
	print 'begin token'
	f=urllib2.urlopen(url);
	print 'end token'
	s=f.read()
	o=urlparse.parse_qs(s)
	token=o['access_token'][0]
	graph_url = "https://graph.facebook.com/me?access_token=%s"%token
	print 'begin id'
	f=urllib2.urlopen(graph_url);
	print 'end id'
	s=f.read()
	jdata=json.loads(s)
	id=jdata['id']
	session['fbUserId']=id
	session['fbSessionToken']=token
	
	print 'begin db'
	g.cur.execute('SELECT user_id FROM Users WHERE facebook_id=%s', id)
	row = g.cur.fetchone()
	print 'end db'
	if (row == None):
		return render_template('register.html')
	else:
		session['userid']=row[0]
	return render_template('main.html', fbUserId=session['fbUserId'])

	
def auth():
	pass