import smtplib, ssl

from email.message import EmailMessage
import mimetypes

class EmailData:
	def __init__(self,subject,body,attachments=None):
		self.subject = subject
		self.body = body
		self.attachments = attachments
	def attachments_to(self,email):
		if self.attachments is not None:
			for attachment in self.attachments:
				guess = mimetypes.guess_type(attachment)
				if guess[0] is None:
					raise Exception()
				main_type,sub_type = guess[0].split("/")
				with open(attachment, "rb") as f:

					email.add_attachment(f.read(),maintype=main_type,subtype=sub_type,filename=attachment.split("/")[-1])

class CompleteMessage:
	def __init__(self,email_addr,smtp_server="gmail.com",sending_warning_mode = True):
		self.email_addr = email_addr
		self.smtp_server = smtp_server
		self.sending_warning_mode = sending_warning_mode

	def set_password(self,password):
		self.password = password

	def _send_email(self,email_data,attachments=None):
		try:
			msg = EmailMessage()
			msg["Subject"] = email_data.subject
			msg["From"] = self.email_addr
			msg["To"] = self.email_addr
			msg.set_content(email_data.body)
			email_data.attachments_to(msg)


			context = ssl.create_default_context()

			with smtplib.SMTP_SSL("smtp."+self.smtp_server,465,context=context) as server:
				#server.starttls(context=context)
				server.login(self.email_addr,self.password)
				server.sendmail(self.email_addr,[self.email_addr],msg.as_string())
		except Exception:
			if self.sending_warning_mode:
				print("WARNING: Could not send email")
			else:
				Exception("Could not send email")
		del self.password

	def send_email_after(self,email_data):
		def decorator(func):
			def wrapper(*args,**kwargs):
				if not hasattr(self,"password"):
					raise Exception("Password is not set!")
				res = func(*args,**kwargs)
				self._send_email(email_data)
				return res
			return wrapper
		return decorator

	def send_function_specific_email(self,func):
		def wrapper(*args,**kwargs):
			if not hasattr(self,"password"):
				raise Exception("Password is not set!")
			res = func(*args,**kwargs)
			self._send_email(res[1])
			return res[0]
		return wrapper

