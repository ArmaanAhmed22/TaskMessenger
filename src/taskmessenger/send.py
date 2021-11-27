from typing import Any, Callable, List, Tuple, Union
import requests
from os.path import basename
from taskmessenger._server_location import location


def get_server_location() -> Tuple[str, str]:
    loc: str = location["LOCATION"]
    port: str = location["PORT"]
    return loc, port


class EmailData:
    """Contains the email data to send a complete message"""
    def __init__(self, subject: str, body: str, attachments: Union[List[str], None] = None):
        """Constructor for EmailData

        Args:
            subject (str): What should appear in the subject of the email
            body (str): Allows for HTML markup of what should appear in the body
            attachments (List[str]): The paths of file attachments of the email
        """
        self.subject = subject
        self.body = body.replace("\n", "<br>")
        self.attachments = attachments if attachments is not None else []


class CompleteMessage:

    _location, _port = get_server_location()

    def __init__(self, email_addr: str, sending_warning_mode: bool = True):
        """Constructor for CompleteMessage

        Args:
            email_addr (str): The email address to send the message to
            sending_warning_mode (bool, optional): Whether to send a warning (True) or raise an exception (False) if POST fails to send message. Defaults to True.
        """
        self.email_addr: str = email_addr
        self.sending_warning_mode: bool = sending_warning_mode

    def _send_email(self, email_data: EmailData):

        attached_files = {}
        opened = []
        for attachment in email_data.attachments:
            file_name = basename(attachment)
            h = open(attachment, "rb")
            attached_files[file_name] = h
            opened.append(h)
        res = requests.post(CompleteMessage._location+":"+CompleteMessage._port, data={"subject": email_data.subject, "body": email_data.body, "to": self.email_addr}, files=attached_files)
        for h in opened:
            h.close()
        return res.status_code

    def send(self, email_data: EmailData):
        self._send_email(email_data)

    def send_email_after(self, email_data: EmailData):
        """Decorator to send message upon completion of function

        Args:
            email_data (EmailData): The email to send
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                self._send_email(email_data)
                return res
            return wrapper
        return decorator

    def send_function_specific_email(self, output_to_email: Callable[[Any], EmailData]):
        """Decorator to send message upon completion of function (depending on specific value of function)

        Args:
            output_to_email (Callable[[Any], EmailData]): turns the output of the function to the EmailData
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                self._send_email(output_to_email(res))
                return res
            return wrapper
        return decorator
