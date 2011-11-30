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
	
@devBluePrint.route('/dms/devgameview')
def devgameview():
	return jsonify(view=render_template('dmsDevGame.html'), addview=render_template('dmsDevAddGame.html'), editview=render_template('dmsDevEditGame.html'))
	
@devBluePrint.route('/dms/devmatchview')
def devmatchview():
	return jsonify(view=render_template('dmsDevMatch.html'), addview=render_template('dmsDevAddMatch.html'), editview=render_template('dmsDevEditMatch.html'))

	