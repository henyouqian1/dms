from dmsMain import *

@mainBluePrint.route('/dms/mainmenuview')
def mainmenuview():
    return render_template('dmsMainMenu.html', email=session['email'], user_id=session['user_id'])