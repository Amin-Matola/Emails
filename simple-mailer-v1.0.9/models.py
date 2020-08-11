
import sqlite3
from PySide2.QtGui import QMessageBox

class Storage(sqlite3, QMessageBox):
	def __init__(self):
		#QSqlDatabase.__init__(self)
		#QSqlQuery.__init__(self)
		#QMessageBox.__init__(self)
		super(Storage,self).__init__()


	def connect(self):
		table 		= """CREATE TABLE IF NOT EXISTS Users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		email TEXT UNIQUE,
		password TEXT)"""

		self.conn 	= self.Connection("users.db");
		self.cur 	= self.conn.cursor()
		try:
			self.cur.execute(table)
			print("Table Created Successfully")
		except:
			self.critical(None, self.tr("Table Creation Error"),self.tr("Table Could not be created"),
				self.Cancel)

	def User(self, username, password):
		self.email = username
		self.password = password
		

		userq = """"INSERT INTO Users VALUES('',%s, %s)"""%(self.email,self.password)
		try:
			self.exec_(q)
			self.exec_(userq)
		except Exception as e:
			return "Oops Oops, that's an error!\n%s"%e