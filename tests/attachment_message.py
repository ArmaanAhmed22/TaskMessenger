from taskmessenger.send import CompleteMessage,EmailData
import getpass

e = EmailData("","",["../__init__.py"])
c = CompleteMessage("user@example.com")
c.set_password(getpass.getpass())
@c.send_email_after(e)
def test():
	#Some code...
	pass

test()
