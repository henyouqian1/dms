from dmsUser import *

@userBluePrint.route('/dms/userview')
def userview():
    return render_template('dmsUser.html')

@userBluePrint.route('/dms/userloginview')
def userloginview():
    return jsonify(view=render_template('dmsUserLogin.html'))
    
@userBluePrint.route('/dms/usermainmenuview')
def usermainmenuview():
    return jsonify(view=render_template('dmsUserMainMenu.html'))
    
@userBluePrint.route('/dms/userregisterview')
def userregisterview():
    return jsonify(view=render_template('dmsUserRegister.html'))