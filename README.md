# TaskMessenger

### Tool to send a designated email after task is finished

## Introduction

Waiting for the termination of a long task can be tedious and unpractical. Instead, it would be useful if an email reminder can be sent automatically at the termination of a task. This package allows for such functionality.

## Requirements
* Python >=3.6

## Installation
From PyPi: `pip install taskmessenger`

From GitHub (newest version): `git clone https://www.github.com/ArmaanAhmed22/taskmessenger & cd taskmessenger & pip install -e .`

## Example:
Sending a message using data from the function:
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
Sending a message inline (without a function):
```python
from taskmessenger.send import CompleteMessage,EmailData

c = CompleteMessage("user@example.com")
c.send(EmailData("SUBJECT","BODY"))
```

## Citation:
Bibtex:
```
@software{armaan_ahmed_2021_5684676,
  author       = {Armaan Ahmed},
  title        = {ArmaanAhmed22/TaskMessenger: TaskMessenger v1.0.0},
  month        = nov,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.5684676},
  url          = {https://doi.org/10.5281/zenodo.5684676}
}
```