
import smtplib, ssl

from email.message import EmailMessage

class EmailData:
	def __init__(self,subject,body):
		self.subject = subject
		self.body = body
class CompleteMessage:
	def __init__(self,email_addr,smtp_server="gmail.com",sending_warning_mode = True):
		self.email_addr = email_addr
		self.smtp_server = smtp_server
		self.sending_warning_mode = sending_warning_mode

	def set_passwd(self,passwd):
		self.passwd = passwd

	def _send_email(self,email_data):
		try:
			msg = EmailMessage()
			msg["Subject"] = email_data.subject
			msg["From"] = self.email_addr
			msg["To"] = self.email_addr
			msg.set_content(email_data.body)

			context = ssl.create_default_context()

			with smtplib.SMTP_SSL("smtp."+self.smtp_server,465,context=context) as server:
				#server.starttls(context=context)
				server.login(self.email_addr,self.passwd)
				server.sendmail(self.email_addr,[self.email_addr],msg.as_string())
		except Exception:
			if self.sending_warning_mode:
				print("WARNING: Could not send email")
			else:
				Exception("Could not send email")
		del self.passwd

	def send_email_after(self,email_data):
		def decorator(func):
			def wrapper(*args,**kwargs):
				if not hasattr(self,"passwd"):
					raise Exception("Password is not set!")
				res = func(*args,**kwargs)
				self._send_email(email_data)
				return res
			return wrapper
		return decorator

	def send_function_specific_email(self,func):
		def wrapper(*args,**kwargs):
			res = func(*args,**kwargs)
			self._send_email(res[1])
			return res[0]
		return wrapper

