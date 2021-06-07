from taskmessenger.send import CompleteMessage,EmailData

c = CompleteMessage("user@example.com") #Use specified email with the default optional arguments
p = input() #Unsafely get password
c.set_passwd(p) #Set the one-time password 

@c.send_function_specific_email #Send email message based on the second element of the tuple
def a(i): #Function will return i**2 and send as an email [Subject: i, Body: i**2]
	return (i**2,EmailData(str(i),str(i**2))) 

print(a(66)) #4356