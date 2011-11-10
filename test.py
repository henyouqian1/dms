import MySQLdb
from random import *
from time import*

class g:
	pass
	

def connectDb():
	g.conn=MySQLdb.connect(host="localhost",user="root",
                  		passwd="verygame123",db="test",charset = "utf8")
	g.cur=g.conn.cursor()
	
def closeDb():
	g.cur.close()
	g.conn.close()
	
def createTable():
	g.cur.execute('''
					DROP TABLE IF EXISTS Scores;
					''')
	g.cur.execute('''
					CREATE TABLE Scores (score_id INTEGER PRIMARY KEY AUTO_INCREMENT,
						score INTEGER NOT NULL) ENGINE = InnoDB;
					''')
	
def insertData():
	for i in xrange(500000):
		g.cur.execute('''
						INSERT INTO Scores (score) VALUES(%i);
					''' % randint(100, 1000000))
	
if __name__ == '__main__':
	t1=time()
	connectDb()
	createTable()
	insertData()
	g.conn.commit()
	closeDb()
	t2=time()
	print('time elapsed:%fsec'%(t2-t1))
	