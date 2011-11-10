from dmsAuth import *

@authBluePrint.route('/dms/loginview')
def loginview():
    return render_template('dmsLogin.html')
    
@authBluePrint.route('/dms/registerview')
def registerview():
	return render_template('dmsRegister.html')