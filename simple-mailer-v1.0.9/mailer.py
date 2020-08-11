from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import *
from PySide2.QtSql import *
import sys,os
from sqlite3 import Connection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL


app			= QApplication(sys.argv)
#---------------------Style------------------

debug 		= True
#--------------------------------------------

class Storage(QMessageBox):
	def __init__(self):
		#QSqlDatabase.__init__(self)
		#QSqlQuery.__init__(self)
		#QMessageBox.__init__(self)
		super(Storage, self).__init__()


	def connect(self):
		table 		= """CREATE TABLE IF NOT EXISTS Users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		email TEXT UNIQUE,
		password TEXT)"""

		self.conn 	= Connection("users.db");
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

storage 	= Storage()




	
#------------------LOGIN CLASS --------------
class User:
	def __init__(self, email, password):
		#global storage

		self.email 		= email.strip("\ ;.,?%*^-=+#@`").lower()
		self.password 	= password.strip()

		if self.email and self.password:
			storage.connect()
			storage.User(self.email, self.password);
		else:
			print("Provide valid data")
			return


		self.servername = ""
		self.done 		= False

		if self.email.endswith("gmail.com"):
			self.server = "smtp.gmail.com"
			self.servername = "Gmail"

		elif self.email.endswith("yahoo.com"):
			self.server = "smtp.mail.yahoo.com"
			self.servername = "Yahoo"

		elif self.email.endswith("hotmail.com"):
			self.server = "smtp.live.com"
			self.servername = "Hotmail"

		elif self.email.endswith("amazon.com"):
			self.server = "email-smtp.us-west-2.amazonaws.com"
			self.servername = "Amazon"

		else:
			self.server = ""


	def login(self):
	
		if self.server:
			try:
				self.server = SMTP_SSL(self.server, 465)
				if debug:
					self.server.set_debuglevel(1)
				self.server.ehlo()
				self.server.login(self.email, self.password)
				logarea.setText("Login %s Successful!..."%self.servername)
				self.done = True

			except Exception as e:
				logarea.setText("Login %s Failed, please try again...\n%s"%(self.servername,e))
			logLayout.addWidget(logarea,0,0)
			
			
			

		else:
			print("No server detected...")
			print("Emain\t:\t%s\nPassword\t:\t%s"%(self.email,self.password))
			changeLabel("",True)
		return self.done
		
	def sendMail(self, to, subject, message):
		msg 			= MIMEMultipart()
		msg.attach(MIMEText(message,"html"))
		msg["From"]		= self.email
		msg["To"] 		= to
		msg["Subject"] 	= subject

		fil 			= MIMEApplication(
										open(r"example.txt","rb").read(), 
										name="styles.css"
										)

		msg.attach(fil)
		try:
			self.server.sendmail(self.email, to, msg.as_string())
			changeLabel("Message Sent Successfully")
		except Exception as e:
			self.server.quit()
			print("That's aweful error\n\n%s"%e)





#-------------Master Window------------------
class Main_Window( QWidget, User ):

	def __init__( self ):
		QWidget.__init__()
		User.__init__()
		self.__width = self.maximumWidth
		self.__width = self.maximumHeight
		self.__style = eval(open("styles.css").read())
		self._layout = QGridLayout()
		self.user 	 = False

		# Main window styles 
		self.setWindowFlags( Qt.FramelessWindowHint)
		self.setStyleSheet( self.__style["main"] )
		self.setMinimumWidth(550)
		self.setMinimumWidth(700)
		self.setMinimumHeight(500)
		self.setWindowTitle( "Simple Mail" )
		self.setAutoFillBackground( True )
		self.setBackgroundRole( QPalette.Highlight )

		self.setup_layout()
		self.setup_widgets()
		self.customize()
		self.setup_functions()


	def login( self ):
	
		if self.server:
			try:
				self.server = SMTP_SSL(self.server, 465)
				if debug:
					self.server.set_debuglevel(1)
				self.server.ehlo()
				self.server.login(self.email, self.password)
				self.logLabel.setText("Login %s Successful!..."%self.servername)
				self.done = True

			except Exception as e:
				self.logLabel.setText("Login %s Failed, please try again...\n%s"%(self.servername, e))
			self.push(self.logLabel, 0, 0)

	def customize(self):

		# Widget styles (Labels)
		self.logLabel.setStyleSheet( self.__style["log_label"] )
		#self.logArea.setStyleSheet( self.__style["log"] )
		
		
		# Email
		self.emailLabel.setStyleSheet( self.__style["flable"] )
		self.emailField.setStyleSheet( self.__style["inputs"] )

		# Password
		self.passLabel.setStyleSheet( self.__style["flable"] )
		self.passField.setStyleSheet( self.__style["inputs"] )


		# Login button
		self.logbtn.setStyleSheet( self.__style["logbtn"] )
		
	def setup_layout( self ):
		# Labels 
		self.logLabel   = QLabel("<h2>Login To Access Your Mailbox...</h2>")
		#self.logArea    = QLabel()

		# Email
		self.emailLabel = QLabel("Your Email")
		self.emailField = QLineEdit()
		self.emailField.setPlaceholderText("Your email address...")

		# Password
		self.passLabel  = QLabel("Password")
		self.passField  = QLineEdit()
		self.passField.setPlaceholderText("insert email password...")
		self.passField.setEchoMode( QLineEdit.Password )

		# Login Button
		self.logbtn     = QPushButton("Login")

		# minimizer icons
		self.minimizer  = QToolButton()
		#self.minimizer.setIcon( QIcon("open.png") )

	def setup_widgets( self ):
		items 	= [self.minimizer, 
				   self.logLabel, 
				   self.emailLabel, 
				   self.emailField, 
				   self.passLabel, 
				   self.passField, 
				   self.logbtn]
		
		for i in range( len(items) ):
			self.push(items[i], i, 0)


	def setup_functions( self ):
		self.minimizer.clicked.connect(lambda: sys.exit())
		self.logbtn.clicked.connect(self.user_manager)
		

	def messenger( self ):
		self._layout 		= QGridLayout()
		self.setStyleSheet( self.__style["othermain"] )

		# Receiver 
		self.toLabel      	= QLabel("To: ")
		self.toLabel.setStyleSheet( self.__style["flable"] )
		self.toField 	  	= QLineEdit()
		self.toField.setPlaceholderText( "Receiver of email")

		# Subject
		self.subjectLabel	= QLabel("Subject: ")
		self.subjectField 	= QLineEdit()
		self.subject.setPlaceholderText("The topic you are to say")
		self.subjectLabel.setStyleSheet( self.__style["flabel"] )

		# Message
		self.message 		= QLineEdit() # styles["text"]
		self.toField.setStyleSheet( self.__style["inputs"] )
		self.subjectField.setStyleSheet( self.__style["inputs"] )
		self.message.setStyleSheet( self.__style["text"] )

		# Buttons ( Submit, Back )
		self.submit			= QPushButton( text = "Send Message" )
		self.back 			= QPushButton( "Back" )

		self.submit.setStyleSheet( self.__style["button"] )
		self.back.setStyleSheet( self.__style["button"] )

		self.submit.clicked.connect(self.grabValues)
		self.messenger_side()

	def push( self, widget, *position):
		self._layout.addWidget(widget, *position)

		
	def messenger_side( self ):
		#----------Control Buttons------------
		self.compose 	= QPushButton(text="Compose")
		self.inbox 		= QPushButton(text="Inbox")
		self.sent 		= QPushButton(text="Sent Mail")
		self.spam 		= QPushButton(text="Spam")
		self.trash 		= QPushButton(text="Trash")
		self.copyright  = QLabel("<h4>Copyright &copy; Amin Apps.</h5>")
		self.indicator 	= QLabel("<h3>Email Control Area</h3>")

		self.push( self.indicator, 0, 1, 1, 2)
		self.push( self.toLabel, 1, 1, 1, 2)
		self.push( self.toField, 2, 1, 1, 2)
		self.push( self.subjectLabel, 3, 1, 1, 2)
		self.push( self.subjectField, 4, 1, 1, 2)
		self.push( self.message, 5, 1, 1, 2)
		self.push(self.back, 6, 1, 1, 1)
		self.push(self.submit, 6, 2)

		self.push( self.compose, 0, 0)
		self.push( self.inbox, 1, 0)
		self.push( self.sent, 2, 0)
		self.push( self.spam, 3, 0)
		self.push( self.trash, 4, 0)
		self.push( self.copyright, 7, 1, 1, 2)


	def dashboard( self, logged = False ):
		if logged:
			self.messenger()
		else:
			self.setLayout( self._layout)
		self.show()

	#------------- User login controller --------
	def user_manager( self ):
		
		self.user = User(self.emailField.text(), self.passField.text())
		if self.user.login():
			self.dashboard(True)

		else:
			print("\nYou are not logged in")


	def grabValues( self ):
		reciever	= self.toField.text()
		top 		= self.subjectField.text()
		mail 		= self.message.toPlainText()

		if self.user:
			try:
				self.user.sendMail(reciever, top, mail)
			except Exception as e:
				print("You are Not loged in...\n\n%s"%e)
				return

	def changeLabel( self, message, log=False):
		if log:
			self.indicator.setText("""Login Successful--Email Control Area.""")
			self.indicator.setStyleSheet(styles["log"])
		else:
			self.indicator.setText("""<h3 style='color:orange;font-size:1.2em;text-align:center;'>%s</h3>"""%message)
		return
	




if __name__	== "__main__":
	window = Main_Window()
	window.dashboard()
	sys.exit( app.exec_() )
