from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import *
import sys
from sqlite3 import Connection
from smtplib import SMTP


#---------------------Style------------------

styles 		= eval(open("styles.css").read())
#--------------------------------------------




#-------------Master Window------------------
app		= QApplication(sys.argv)

class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setStyleSheet(styles["main"])
		self.setMinimumWidth(550)
		self.setMinimumHeight(500)
		self.setMaximumWidth(700)
		self.setWindowTitle("Email Sender.")
		self.setAutoFillBackground(True)
		self.setBackgroundRole(QPalette.Highlight)

#--------------------------------------------

#-------------Models-------------------------
# table	= Connection("logtable.db")
# cursor	= table.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS login(
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# email UNIQUE NOT NULL,
# password TEXT)""")

class Connection(QSqlDatabase,QMessageBox):
	def __init__(self):
		QSqlDatabase.__init__(self)
		QMessageBox.__init__(self)
	def connect(self):
		self.addDatabase('QODBC')
		self.setDatabaseName('emails.db')

		if not self.open():
			self.critical(None,
			self.tr("Database Error"),
			self.tr("Unable to establish connection"),
			self.Cancel)
		return False

#------------------LOGIN WINDOW--------------
logLabel= QLabel("<h2 style='text-align:center'>Login To Access Your Mailbox...</h2>")
logLabel.setStyleSheet("""
width:100%;
border:none;
font-size:2em;
color:orange;
text-align:center;
margin-top:2px;
margin:10px;
margin-bottom:25px;
	""")
logarea = QLabel()
logarea.setStyleSheet("""border:none""")
emLabel	= QLabel("Your Email")
emLabel.setStyleSheet(styles["flable"])

#-----------------Email Input-------------------------
emInp	= QLineEdit()
emInp.setPlaceholderText("Your email address...")
emInp.setStyleSheet(styles["inputs"])
pasLabel= QLabel("Password")
pasLabel.setStyleSheet(styles["flable"])

#-----------------Password----------------------------
pasInp	= QLineEdit()
pasInp.setEchoMode(QLineEdit.Password)
pasInp.setStyleSheet(styles["inputs"])
pasInp.setPlaceholderText("insert email password...")
logbtn 	= QPushButton("Login")
logbtn.setStyleSheet("""
	background:#5e5efe;
	height:25px;
	color:white;
	border:1px solid white;
	font-size:17px;
	margin:20px;
	margin-bottom:30px;
	margin-top:30px""")
minms 	= QToolButton()
minms.setIcon(QIcon("img/min.png"))
logLayout=QGridLayout()
logLayout.addWidget(minms,0,0)
#logLayout.addWidget(logarea,0,0)
logLayout.addWidget(logLabel,1,0)
logLayout.addWidget(emLabel,2,0)
logLayout.addWidget(emInp,3,0)
logLayout.addWidget(pasLabel,4,0)
logLayout.addWidget(pasInp,5,0)
logLayout.addWidget(logbtn,6,0)



minms.clicked.connect(lambda: sys.exit())


#--------------------------------------------
layout 	= QGridLayout()

from_lab= QLabel("FROM")
from_lab.setStyleSheet(styles["flable"])
from_	= QLineEdit()
from_.setStyleSheet(styles["inputs"])
from_.setPlaceholderText("Your email here...")

to_lab 	= QLabel("TO")
to_lab.setStyleSheet(styles["flable"])
to 		= QLineEdit()
to.setStyleSheet(styles["inputs"])
to.setPlaceholderText("Reciever's email...")
message = QTextEdit()
message.setStyleSheet(styles["text"])
submit	= QPushButton(
	text="Send Message")
submit.setStyleSheet(styles["button"])
#----------Control Buttons------------
compose = QPushButton(text="Compose")
inbox 	= QPushButton(text="Inbox")
sent 	= QPushButton(text="Sent Mail")
spam 	= QPushButton(text="Spam")
trash 	= QPushButton(text="Trash")

#window.setMaximumWidth(compose.maximumWidth()*2)
#-------------------------------------

def sendEmail(sender, reciever, mail):
	print("From : %s\nto: %s\nMessage: %s"%(
		sender,
		reciever,
		mail))



def grabValues():
	sender	= from_.text()
	reciever= to.text()
	mail 	= message.toPlainText()

	sendEmail(sender,reciever,mail)
	

#--------------controls------------------------
layout.addWidget(compose,0,0)
layout.addWidget(inbox,1,0)
layout.addWidget(sent,2,0)
layout.addWidget(spam,3,0)
layout.addWidget(trash,4,0)
lab2 = QLabel("<h4 style='text-align:center'><i style='font-size:12px;width:100%;'>Copyright &copy; Amin Apps.</i></h5>")

layout.addWidget(lab2,7,1)
#--------------------------------------

#-----------main label-----------------
l1		= QLabel("""
	<h3 style='
	text-align:center;
	font-size:2em;
	color:orange;'>
	Email Control Area
	</h3>""")

def changeLabel(x):
	l1.setText("""
		<h3 style='
		color:orange;
		font-size:1.2em;
		text-align:center;'>
		Control your %s </h3>"""%x)
	return
contWin 	= QWidget()
contWin.setWindowTitle("Email Manipulator.")
contWin.setWindowIcon(QIcon("file:///C:/Users/Coder/Pictures/qt1.PNG"))
contWin.setMinimumWidth(550)
contWin.setMinimumHeight(490)
contWin.setMaximumWidth(700)
contWin.setStyleSheet(styles["othermain"])
#-------------DashBoard----------------------
def dashboard():
	window = Window()
	window.setVisible(False)
	window = contWin
	window.setLayout(layout)
	window.show()

def login():
	global serv
	email 	= emInp.text()
	password= pasInp.text()
	if email.strip().endswith("gmail.com"):
		try:
			serv=SMTP("smtp.gmail.com",587)
			serv.ehlo()
			serv.starttls()
			serv.ehlo()
		
			serv.login(email,password)
		except:
			logarea.setText("<h3 style='color:red;text-align:center'>Login Failed, please try again...</h1>")
			logLayout.addWidget(logarea,0,1)
			return

	print("Emain\t:\t%s\nPassword\t:\t%s"%(email,password))
	dashboard()

submit.clicked.connect(grabValues)
logbtn.clicked.connect(login)

inbox.clicked.connect(lambda:changeLabel("Inbox"))

layout.addWidget(l1,0,1)
layout.addWidget(from_lab,1,1)
layout.addWidget(from_,2,1)
layout.addWidget(to_lab,3,1)
layout.addWidget(to,4,1)
layout.addWidget(message,5,1)
layout.addWidget(submit,6,1)


if __name__	== "__main__":
	window = Window()
	window.setLayout(logLayout)
	#print(window.maximumSize())
	window.show()
	sys.exit(app.exec_())
