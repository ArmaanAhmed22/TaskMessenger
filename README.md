# TaskMessenger

### Tool to send a designated email after task is finished

## Introduction

Waiting for the termination of a long task can be tedious and unpractical. Instead, it would be useful if an email reminder can be sent automatically at the termination of a task. This package allows for such functionality.

## Requirements
* Python >=3.6

## Installation
`pip install taskmessenger`

## Example:
Sending a message within the function:
```python
from taskmessenger.send import CompleteMessage,EmailData

c = CompleteMessage("user@example.com") #Use specified email with the default optional arguments

@c.send_function_specific_email(lambda x: EmailData("Output from 'a'",str(x))) #Send email message based on the second element of the tuple
def a(i): #Function will return i**2 and send as an email [Subject: i, Body: i**2]
    return (i**2,EmailData(str(i),str(i**2))) 

print(a(66)) #4356
```
Sending a function value-independent message:
```python
from taskmessenger.send import CompleteMessage,EmailData

c = CompleteMessage("user@example.com")

e = EmailData("SUBJECT","BODY")
@c.send_email_after(e) #Send message
def func():
	print("Doing something...")

func()
```
