
import smtplib, ssl

from email.message import EmailMessage

class CompleteMessage:
	def __init__(self,email_addr,smtp_server="gmail.com"):
		self.email_addr = email_addr
		self.smtp_server = smtp_server

	def set_passwd(self,passwd):
		self.passwd = passwd

	def _send_email(self,subject,message):
		msg = EmailMessage()
		msg["Subject"] = subject
		msg["From"] = self.email_addr
		msg["To"] = self.email_addr
		msg.set_content(message)

		context = ssl.create_default_context()

		with smtplib.SMTP_SSL("smtp."+smtp_server,465,context=context) as server:
			#server.starttls(context=context)
			server.login(self.email_addr,self.passwd)
			server.sendmail(self.email_addr,[self.email_addr],msg.as_string())
		del self.passwd

	def send_email_after(self,subject,message):
		def decorator(func):
			def wrapper(*args,**kwargs):
				res = func(*args,**kwargs)
				self._send_email(subject,message)
				return res
			return wrapper
		return decorator


c = CompleteMessage("aahmedresearch@gmail.com")
c.set_passwd("Ladz67azrm314aa201982")


@c.send_email_after("THIS IS WRAPPER","")
def t():
	return 8
print(t())

