from dmsDev import *

@devBluePrint.route('/dms/devloginview')
def devloginview():
    return render_template('dmsDevLogin.html')
    
@devBluePrint.route('/dms/devregisterview')
def devregisterview():
	return render_template('dmsDevRegister.html')
	
@devBluePrint.route('/dms/devmainmenuview')
def devdevmainmenuview():
	id = ''
	email = ''
	try:
		id=session['developer_id']
		email=session['developer_email']
	except:
		return redirect(url_for('.devloginview', _external=True))
	return render_template('dmsDevMainMenu.html', developer_email=email, developer_id=id)
	
@devBluePrint.route('/dms/devawardview')
def devaward():
	return render_template('dmsDevAward.html')