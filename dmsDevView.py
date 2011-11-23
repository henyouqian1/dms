from dmsDev import *

@devBluePrint.route('/dms/devview')
def devview():
    return render_template('dmsDev.html')
    
@devBluePrint.route('/dms/devloginview')
def devloginview():
    return jsonify(view=render_template('dmsDevLogin.html'))
    
@devBluePrint.route('/dms/devregisterview')
def devregisterview():
	return jsonify(view=render_template('dmsDevRegister.html'))
	
@devBluePrint.route('/dms/devmainmenuview')
def devmainmenuview():
	return jsonify(view=render_template('dmsDevMainMenu.html'))
	
@devBluePrint.route('/dms/devawardview')
def devawardview():
	return jsonify(view=render_template('dmsDevAward.html'), addview=render_template('dmsDevAddAward.html'), editview=render_template('dmsDevEditAward.html'))
	