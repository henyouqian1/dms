from flask import *
import MySQLdb
from dmsConfig import *

mainBluePrint = Blueprint('main', __name__)

@mainBluePrint.route('/dms/xx')
def xx():
	return jsonify(login=0)
